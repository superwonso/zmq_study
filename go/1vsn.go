package main

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/pebbe/zmq4"
)

func main() {
	publisher, _ := zmq4.NewSocket(zmq4.Type(zmq4.PUB))
	defer publisher.Close()

	publisher.Bind("tcp://*:5556")
	publisher.Bind("ipc://weather.ipc")

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	// loop for a while aparently
	for {

		//  make values that will fool the boss
		zipcode := rand.Intn(100000)
		temperature := rand.Intn(215) - 80
		relhumidity := rand.Intn(50) + 10

		msg := fmt.Sprintf("%d %d %d", zipcode, temperature, relhumidity)

		//  Send message to all subscribers
		publisher.Send(msg, 0)
	}
}
