//
// Created by James Nolan on 18/8/21.
//

#include "hsj_helper.h"
#include <iostream>
#include <cstdlib>

#define CAPACITY 1024

class HSJ_Queue {
    int *array; //Here the type needs to change.
    int capacity;
    int first_element;
    int last_element;
    int size;
public:
    explicit HSJ_Queue(int capacity = CAPACITY);

    ~HSJ_Queue();

    void dequeue();

    void enqueue(int element);

    int get_size() const;

    bool isEmpty() const;

    bool isFull() const;
};

HSJ_Queue::HSJ_Queue(int capacity):capacity(capacity){
    array = new int[size];
}

HSJ_Queue::~HSJ_Queue() {
    delete[] array;
}

void HSJ_Queue::dequeue() {

    this->size--;
}

void HSJ_Queue::enqueue(int element) {

    this->size++;
}

int HSJ_Queue::get_size() const {
    return size;
}

bool HSJ_Queue::isEmpty() const {
    return size == 0;
}

bool HSJ_Queue::isFull() const {
    return size >= capacity;
}
