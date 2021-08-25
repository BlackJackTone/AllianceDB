//
// Created by Wang Chenyu on 18/8/21.
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

    int peek();

    int get_size() const;

    bool isEmpty() const;

    bool isFull() const;
};

HSJ_Queue::HSJ_Queue(int capacity):capacity(capacity){
    array = new int[size];
    first_element = 0;
    last_element = -1;
    size = 0;
}

HSJ_Queue::~HSJ_Queue() {
    delete[] array;
}

void HSJ_Queue::dequeue() {
    if (isEmpty()) return;
    first_element = (first_element + 1) % capacity;
    this->size--;
}

void HSJ_Queue::enqueue(int item) {
    if (isFull()) {
        this->dequeue();
        this->enqueue(item);
    }
    last_element = (last_element + 1) % capacity;
    array[last_element] = item;
    this->size++;
}

int HSJ_Queue::peek() {
    if (isEmpty()) return -1;
    return array[first_element];
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