$(document).ready(function(){
    $('.gua-comment-add').on('click', function(){
        console.log('add button')
        var button = $(this)
        var parent = button.parent()
        var weibo_id = parent.find('.gua-comment-weibo_id').val()
        console.log('weibo', weibo_id)
        var content = parent.find('.gua-comment-content').val()
        console.log('content', content)

        var commentList = parent.parent().find('.gua-comment-list')
        console.log('commentList', commentList)

        var weibo = {
            'weibo_id': weibo_id,
            'content': content
        }
        var request = {
            url: '/api/comment/add',
            type: 'post',
            data: weibo,
            success: function() {
                console.log('成功', arguments)
                var response = arguments[0]
                var comment = JSON.parse(response)
                var content = comment.content
                var cell = `
                    <div class="gua-comment-cell">
                        ${content}
                    </div>
                `;
                commentList.append(cell)

            },
            error: function() {
                console.log('错误', arguments)
            }
        }
        $.ajax(request)
    })
    })