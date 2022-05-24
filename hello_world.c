#include "zmq.h"
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>

int main() {
    void *context = zmq_ctx_new();
    void *responder = zmq_socket(context, ZMQ_REP);
    int rc = zmq_bind(responder, "tcp://*:5555");
    assert(rc == 0);
    while(true ) {
        char buffer[10];
        zmq_recv(responder, buffer, 10, 0);
        printf("Received: %s\n", buffer);
        sleep(1);
        zmq_send(responder, "World", 5, 0);
    }
    return 0;
}
