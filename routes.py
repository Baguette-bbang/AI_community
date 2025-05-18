@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        # ... existing code ...
        is_anonymous = 'is_anonymous' in request.form
        post = Post(
            title=title,
            content=content,
            author=current_user,
            is_anonymous=is_anonymous
        )
        # ... existing code ...

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    # ... existing code ...
    is_anonymous = 'is_anonymous' in request.form
    comment = Comment(
        content=content,
        author=current_user,
        post=post,
        is_anonymous=is_anonymous
    )
    # ... existing code ... 