package main

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/pebbe/zmq4"
)

func main() {
	Publisher, _ := zmq4.NewSocket(zmq4.PUB)
	defer Publisher.Close()
	Publisher.Bind("tcp://*:5556")
	Publisher.Bind("ipc://weather.ipc")

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
		Publisher.Send(msg, 0)
	}
}
