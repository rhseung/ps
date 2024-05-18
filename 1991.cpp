#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using node = struct node {
    char name;
    node *left;
    node *right;
};

node *find(node *head, char name) {
    if (head == nullptr)
        return nullptr;
    else if (head->name == name)
        return head;

    node *found = find(head->left, name);
    if (found == nullptr)
        found = find(head->right, name);

    return found;
}

void preorder(node *v) {
    if (v != nullptr) {
        cout << v->name;
        preorder(v->left);
        preorder(v->right);
    }
}

void inorder(node *v) {
    if (v != nullptr) {
        inorder(v->left);
        cout << v->name;
        inorder(v->right);
    }
}

void postorder(node *v) {
    if (v != nullptr) {
        postorder(v->left);
        postorder(v->right);
        cout << v->name;
    }
}

void $(node* head) {
    preorder(head);
    cout << endl;
    inorder(head);
    cout << endl;
    postorder(head);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    cin >> n;

    // _ABCD_EF_______G

    node *head = new node();
    head->name = 'A';

    for (int i = 0; i < n; ++i) {
        char a, b, c;
        cin >> a >> b >> c;

        node *root = find(head, a);

        if (b != '.') {
            node *left = new node();
            left->name = b;
            root->left = left;
        }

        if (c != '.') {
            node *right = new node();
            right->name = c;
            root->right = right;
        }
    }

    $(head);
}
