package eventbus

import (
	"reflect"
	"sync"
	"time"

	"github.com/OWASP/Amass/utils"
)

type pubReq struct {
	Topic string
	Args  []reflect.Value
}

// EventBus handles sending and receiving events across Amass.
type EventBus struct {
	sync.Mutex
	topics map[string][]reflect.Value
	max    utils.Semaphore
	queue  *utils.Queue
	done   chan struct{}
}

// NewEventBus initializes and returns an EventBus object.
func NewEventBus() *EventBus {
	eb := &EventBus{
		topics: make(map[string][]reflect.Value),
		max:    utils.NewSimpleSemaphore(1000000),
		queue:  new(utils.Queue),
		done:   make(chan struct{}, 2),
	}
	go eb.processRequests()
	return eb
}

// Subscribe registers callback to be executed for all requests on the channel.
func (eb *EventBus) Subscribe(topic string, fn interface{}) {
	if topic == "" || reflect.TypeOf(fn).Kind() != reflect.Func {
		return
	}

	callback := reflect.ValueOf(fn)

	eb.Lock()
	eb.topics[topic] = append(eb.topics[topic], callback)
	eb.Unlock()
}

// Unsubscribe deregisters the callback from the channel.
func (eb *EventBus) Unsubscribe(topic string, fn interface{}) {
	if topic == "" || reflect.TypeOf(fn).Kind() != reflect.Func {
		return
	}

	callback := reflect.ValueOf(fn)

	eb.Lock()
	defer eb.Unlock()

	var channels []reflect.Value
	for _, c := range eb.topics[topic] {
		if c != callback {
			channels = append(channels, c)
		}
	}
	eb.topics[topic] = channels
}

// Publish sends req on the channel labeled with name.
func (eb *EventBus) Publish(topic string, args ...interface{}) {
	if topic == "" {
		return
	}

	passedArgs := make([]reflect.Value, 0)
	for _, arg := range args {
		passedArgs = append(passedArgs, reflect.ValueOf(arg))
	}

	eb.queue.Append(&pubReq{
		Topic: topic,
		Args:  passedArgs,
	})
}

func (eb *EventBus) processRequests() {
	curIdx := 0
	maxIdx := 7
	delays := []int{10, 25, 50, 75, 100, 150, 250, 500}

	for {
		select {
		case <-eb.done:
			return
		default:
			element, ok := eb.queue.Next()
			if !ok {
				if curIdx < maxIdx {
					curIdx++
				}
				time.Sleep(time.Duration(delays[curIdx]) * time.Millisecond)
				continue
			}

			curIdx = 0
			p := element.(*pubReq)

			eb.Lock()
			callbacks, found := eb.topics[p.Topic]
			eb.Unlock()

			if found {
				eb.max.Acquire(1)
				go eb.executeCallbacks(callbacks, p.Args)
			}
		}
	}
}

func (eb *EventBus) executeCallbacks(callbacks, args []reflect.Value) {
	defer eb.max.Release(1)

	for _, cb := range callbacks {
		cb.Call(args)
	}
}

// Stop prevents any additional requests from being sent.
func (eb *EventBus) Stop() {
	close(eb.done)
}
