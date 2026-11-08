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


class Nodes:
    def __init__(self, data):
        self.data = data
        self.next = None

class InfixToPostfix:
    def __init__(self):
        self.stack = []
        self.output = []

    def is_operator(self, c):
        return c in ['+', '-', '*', '/', '^']

    def precedence(self, op):
        if op == '+' or op == '-':
            return 1
        elif op == '*' or op == '/':
            return 2
        elif op == '^':
            return 3
        return 0

    def infix_to_postfix(self, expression):
        for char in expression:
            if char.isalnum():
                self.output.append(char)
            elif char == '(': 
                self.stack.append(char)
            elif char == ')': 
                while self.stack and self.stack[-1] != '(':
                    self.output.append(self.stack.pop())
                self.stack.pop() 
            elif self.is_operator(char): 
                while (self.stack and self.precedence(self.stack[-1]) >= self.precedence(char)):
                    self.output.append(self.stack.pop())
                self.stack.append(char)

        while self.stack:
            self.output.append(self.stack.pop())

        return ''.join(self.output)

@app.route('/works/area/infix_to_postfix', methods=['GET', 'POST'])
def infix_to_postfix():
    postfix = None
    stack = []
    if request.method == 'POST':
        expression = request.form.get('infix', '')
        converter = InfixToPostfix()
        postfix = converter.infix_to_postfix(expression)
        stack = converter.stack
    return render_template('InfixToPostfix.html', postfix=postfix, stack=stack)

@app.route('/works/area/enque_dequeue', methods=['GET', 'POST'])
def enque_dequeue():
    queue = session.get('queue', [])
    message = None
    category = 'success'

    if request.method == 'POST':
        action = request.form.get('action', '')
        value = request.form.get('value', '').strip()

        if action == 'enqueue':
            if not value:
                message = 'Enter a value to enqueue.'
                category = 'error'
            else:
                queue.append(value)
                message = f'Enqueued {value}.'
        elif action == 'dequeue':
            if not queue:
                message = 'The queue is empty. Cannot dequeue.'
                category = 'error'
            else:
                removed_value = queue.pop(0)
                message = f'Dequeued {removed_value}.'
        elif action == 'clear':
            queue.clear()
            message = 'Cleared the queue.'
        else:
            message = 'Choose a valid queue operation.'
            category = 'error'

        session['queue'] = queue
        flash(message, category)
        return redirect(url_for('enque_dequeue'))

    return render_template('enque_dequeue.html', queue=queue)

@app.route('/works/area/sorting', methods=['GET', 'POST'])
def sorting():
    sorted_list = []
    if request.method == 'POST':
        numbers = request.form.get('numbers', '').split(',')
        numbers = [int(x.strip()) for x in numbers if x.strip()]
        sorted_list = sorted(numbers)
    return render_template('sorting.html', sorted_list=sorted_list)

@app.route('/works/area/binary_tree', methods=['GET', 'POST'])
def binary_tree():
    tree = BinaryTree()
    tree.restore(
        session.get('binary_tree'),
        session.get('binary_tree_values', []),
    )

    if request.method == 'POST':
        operation = request.form.get('operation', '')
        if operation == 'preorder_traversal':
            traversal_name = 'Preorder'
            traversal = tree.preorder(tree.root)
        elif operation == 'inorder_traversal':
            traversal_name = 'Inorder'
            traversal = tree.inorder(tree.root)
        elif operation == 'postorder_traversal':
            traversal_name = 'Postorder'
            traversal = tree.post_traversal(tree.root, [])
        else:
            traversal = None

        if traversal is not None:
            session['binary_tree_traversal'] = traversal
            session['binary_tree_traversal_name'] = traversal_name
        else:
            try:
                value = int(request.form.get('tree-value', '').strip())
            except ValueError:
                flash('Enter a whole number to perform this operation.', 'error')
                return redirect(url_for('binary_tree'))

            session.pop('binary_tree_traversal', None)
            session.pop('binary_tree_traversal_name', None)
            if operation == 'insert':
                if tree.root is None:
                    tree.root = BinaryTreeNode(value)
                    flash(f'Inserted {value} as the root node.', 'success')
                else:
                    try:
                        parent = int(request.form.get('tree-parent', '').strip())
                    except ValueError:
                        flash('Choose an existing parent node.', 'error')
                        return redirect(url_for('binary_tree'))

                    side = request.form.get('tree-side', '')
                    inserted, message = tree.insert_as_child(parent, side, value)
                    flash(
                        f'Inserted {value} as the {side} child of {parent}.'
                        if inserted else message,
                        'success' if inserted else 'error',
                    )
            elif operation == 'search':
                if tree.search(tree.root, value) is not None:
                    flash(f'{value} was found in the tree.', 'success')
                else:
                    flash(f'{value} was not found in the tree.', 'error')
            elif operation == 'delete':
                if tree.search(tree.root, value) is None:
                    flash(f'{value} was not found in the tree.', 'error')
                else:
                    tree.root = tree.delete_node(tree.root, value)
                    flash(f'Deleted {value} from the tree.', 'success')
            else:
                flash('Choose a valid tree operation.', 'error')

        session['binary_tree'] = tree.serialize(tree.root)
        session.pop('binary_tree_values', None)
        return redirect(url_for('binary_tree'))

    return render_template(
        'binary_tree.html',
        tree_visualization=render_binary_tree(tree.root),
        node_count=len(tree.preorder(tree.root)),
        tree_values=tree.preorder(tree.root),
        traversal=session.get('binary_tree_traversal'),
        traversal_name=session.get('binary_tree_traversal_name'),
    )


class BinaryTreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def restore(self, snapshot, legacy_values):
        if isinstance(snapshot, dict):
            self.root = self.deserialize(snapshot)
            return

        # Migrate sessions created before the tree stored its child structure.
        for value in legacy_values:
            if self.root is None:
                self.root = BinaryTreeNode(value)
                continue
            queue = [self.root]
            index = 0
            while index < len(queue):
                parent = queue[index]
                index += 1
                if parent.left is None:
                    parent.left = BinaryTreeNode(value)
                    break
                if parent.right is None:
                    parent.right = BinaryTreeNode(value)
                    break
                queue.extend((parent.left, parent.right))

    def serialize(self, root):
        if root is None:
            return None
        return {
            'data': root.data,
            'left': self.serialize(root.left),
            'right': self.serialize(root.right),
        }

    def deserialize(self, snapshot):
        node = BinaryTreeNode(snapshot['data'])
        if isinstance(snapshot.get('left'), dict):
            node.left = self.deserialize(snapshot['left'])
        if isinstance(snapshot.get('right'), dict):
            node.right = self.deserialize(snapshot['right'])
        return node

    def insert_as_child(self, parent_value, side, data):
        if side not in ('left', 'right'):
            return False, 'Choose whether to insert on the left or right.'
        if self.search(self.root, data) is not None:
            return False, f'{data} is already in the tree.'

        parent = self.search(self.root, parent_value)
        if parent is None:
            return False, 'Choose an existing parent node.'
        if getattr(parent, side) is not None:
            return False, f'{parent_value} already has a {side} child.'

        setattr(parent, side, BinaryTreeNode(data))
        return True, ''

    def search(self, root, key):
        if root is None or root.data == key:
            return root
        found = self.search(root.left, key)
        return found if found is not None else self.search(root.right, key)

    def post_traversal(self, start, traversal):
        if start is not None:
            self.post_traversal(start.left, traversal)
            self.post_traversal(start.right, traversal)
            traversal.append(start.data)
        return traversal

    def inorder(self, root):
        if root is None:
            return []
        return (
            self.inorder(root.left)
            + [root.data]
            + self.inorder(root.right)
        )

    def delete_node(self, root, key):
        if root is None:
            return None

        queue = [(root, None)]
        target = None
        deepest = None
        deepest_parent = None
        index = 0
        while index < len(queue):
            node, parent = queue[index]
            index += 1
            if node.data == key and target is None:
                target = node
            deepest = node
            deepest_parent = parent
            if node.left is not None:
                queue.append((node.left, node))
            if node.right is not None:
                queue.append((node.right, node))

        if target is None or deepest is None:
            return root
        if target is deepest:
            if deepest_parent is None:
                return None
            if deepest_parent.left is deepest:
                deepest_parent.left = None
            else:
                deepest_parent.right = None
            return root

        target.data = deepest.data
        if deepest_parent.left is deepest:
            deepest_parent.left = None
        else:
            deepest_parent.right = None
        return root

    def preorder(self, root):
        if root is None:
            return []
        return (
            [root.data]
            + self.preorder(root.left)
            + self.preorder(root.right)
        )


def render_binary_tree(root):
    if root is None:
        return (
            '<div class="binary-tree-empty">'
            '<span class="binary-tree-empty-icon" aria-hidden="true">+</span>'
            '<strong>Your tree is empty</strong>'
            '<span>Insert a number to create the root node.</span>'
            '</div>'
        )

    positions = {}
    ordered_nodes = []
    depths = {}
    max_depth = 0

    def collect_nodes(node, depth):
        nonlocal max_depth
        if node is None:
            return
        collect_nodes(node.left, depth + 1)
        depths[id(node)] = depth
        ordered_nodes.append(node)
        max_depth = max(max_depth, depth)
        collect_nodes(node.right, depth + 1)

    collect_nodes(root, 0)
    left_count = next(index for index, node in enumerate(ordered_nodes) if node is root)
    right_count = len(ordered_nodes) - left_count - 1
    width = max(560, (2 * max(left_count, right_count) + 1) * 84 + 72)
    height = max(180, 72 + (max_depth + 1) * 92)
    root_center_x = width // 2
    for index, node in enumerate(ordered_nodes):
        positions[id(node)] = (
            root_center_x + (index - left_count) * 84,
            36 + depths[id(node)] * 92,
        )
    edges = []
    nodes = []

    for node in ordered_nodes:
        x, y = positions[id(node)]
        for child in (node.left, node.right):
            if child is not None:
                child_x, child_y = positions[id(child)]
                edges.append(
                    f'<line class="binary-tree-edge" x1="{x}" y1="{y}" '
                    f'x2="{child_x}" y2="{child_y}" '
                    'stroke="#9aacc0" stroke-width="2.5" />'
                )
        node_class = 'binary-tree-node binary-tree-root' if node is root else 'binary-tree-node'
        nodes.append(
            f'<g class="{node_class}"><circle cx="{x}" cy="{y}" r="25" fill="#e8f3fc" '
            'stroke="#0a66c2" stroke-width="3" />'
            f'<text x="{x}" y="{y}" dominant-baseline="middle" '
            'text-anchor="middle" fill="#253247" font-size="13" '
            f'font-family="sans-serif" font-weight="700">{node.data}</text></g>'
        )

    return (
        f'<svg class="binary-tree-svg" role="img" '
        f'aria-label="Binary tree with {len(ordered_nodes)} nodes" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'{"".join(edges)}{"".join(nodes)}</svg>'
    )

if __name__ == "__main__":
    app.run(debug=True)
