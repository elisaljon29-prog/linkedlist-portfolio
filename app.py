import os

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works', methods=['GET', 'POST'])
def works():
    return render_template('works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/works/touppercase', methods=['GET', 'POST'])
def touppercase():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()
    return render_template('touppercase.html', result=result)

@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    if request.method == 'POST':
        radius = request.form.get('radius', '')
        result = int(radius)*3.14*int(radius)
    return render_template('circle.html', result=result)

@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None
    if request.method == 'POST':
        base = request.form.get('base', '')
        height = request.form.get('height', '')
        result = 0.5 * int(base) * int(height)
    return render_template('triangle.html', result=result)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
            self.head = new_node
        else:
            self.head = new_node
            self.tail = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head:
            self.tail.next = new_node
            self.tail = new_node
        else:
            self.tail = new_node
            self.head = new_node

    def values(self):
        values = []
        current_node = self.head
        while current_node:
            values.append(current_node.data)
            current_node = current_node.next
        return values

    def search(self, data):
        current_node = self.head
        while current_node:
            if current_node.data == data:
                return True
            current_node = current_node.next
        return False

    def printLinkedList(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

    def remove_beginning(self):
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return data

    def remove_at_end(self):
        if self.head is None:
            return None
        elif self.head == self.tail:
            data = self.head.data
            self.head = None
            self.tail = None
            return data

        current_node = self.head
        while current_node.next != self.tail:
            current_node = current_node.next
        data = self.tail.data
        current_node.next = None
        self.tail = current_node
        return data

    def remove_at(self, data):
        if self.head is None:
            return None
        elif self.head.data == data:
            return self.remove_beginning()

        current_node = self.head
        while current_node.next is not None:
            if current_node.next.data == data:
                removed_data = current_node.next.data
                current_node.next = current_node.next.next
                if current_node.next is None:
                    self.tail = current_node
                return removed_data
            current_node = current_node.next
        return None

    def insert_after(self, nodedata, data):
        current_node = self.head
        while current_node is not None:
            if current_node.data == nodedata:
                new_node = Node(data)
                new_node.next = current_node.next
                current_node.next = new_node
                if new_node.next is None:
                    self.tail = new_node
                return True
            current_node = current_node.next
        return False


@app.route('/works/area/linklist', methods=['GET', 'POST'])
def linklist():
    values = session.get('linklist_values')
    if values is None:
        values = ['10', '20', '30']
        session['linklist_values'] = values

    linked_list = LinkedList()
    for value in values:
        linked_list.insert_at_end(value)

    if request.method == 'POST':
        action = request.form.get('action', '')
        value = request.form.get('value', '').strip()
        target = request.form.get('target', '').strip()
        message = None
        category = 'success'

        if action in ('insert_beginning', 'insert_end', 'search', 'remove_value'):
            if not value:
                message = 'Enter a value to perform this operation.'
                category = 'error'
            elif action == 'insert_beginning':
                linked_list.insert_at_beginning(value)
                message = f'Added {value} to the beginning.'
            elif action == 'insert_end':
                linked_list.insert_at_end(value)
                message = f'Added {value} to the end.'
            elif action == 'search':
                if linked_list.search(value):
                    message = f'{value} is in the linked list.'
                else:
                    message = f'{value} is not in the linked list.'
                    category = 'error'
            else:
                removed = linked_list.remove_at(value)
                if removed is None:
                    message = f'{value} was not found in the linked list.'
                    category = 'error'
                else:
                    message = f'Removed {removed} from the linked list.'
        elif action == 'remove_beginning':
            removed = linked_list.remove_beginning()
            message = (
                f'Removed {removed} from the beginning.'
                if removed is not None else 'The linked list is already empty.'
            )
            category = 'success' if removed is not None else 'error'
        elif action == 'remove_end':
            removed = linked_list.remove_at_end()
            message = (
                f'Removed {removed} from the end.'
                if removed is not None else 'The linked list is already empty.'
            )
            category = 'success' if removed is not None else 'error'
        elif action == 'insert_after':
            new_value = request.form.get('new_value', '').strip()
            if not target or not new_value:
                message = 'Enter both the target value and the new value.'
                category = 'error'
            elif linked_list.insert_after(target, new_value):
                message = f'Inserted {new_value} after {target}.'
            else:
                message = f'{target} was not found in the linked list.'
                category = 'error'
        elif action == 'clear':
            linked_list = LinkedList()
            message = 'Cleared the linked list.'
        elif action == 'reset':
            linked_list = LinkedList()
            for starter_value in ('10', '20', '30'):
                linked_list.insert_at_end(starter_value)
            message = 'Restored the starter list: 10 → 20 → 30.'
        else:
            message = 'Choose a valid linked-list operation.'
            category = 'error'

        session['linklist_values'] = linked_list.values()
        flash(message, category)
        return redirect(url_for('linklist'))

    return render_template('linklist.html', values=values)


if __name__ == "__main__":
    app.run(debug=True)
