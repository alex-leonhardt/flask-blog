import markdown
from flask import Flask
from flask import render_template
from flask import Markup
from flask.ext.cache import Cache
import logging
import os
import re

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
POSTS_DIR='{0}/posts'.format(BASE_DIR)

COPYRIGHT='MY_BLOG'
BLOG_NAME='MY_BLOG'
SUB_HEADING='A blog that\'s out of this world.'
ABOUT_HEADING='About me'
ABOUT_SUB='Just a another geek with another blog.'

TWITTER_LINK=''
FACEBOOK_LINK=''
GITHUB_LINK=''

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

default_cache_timeout = 2678400 # 31 days

def unsanitize(s):
    s = re.sub('\ ', '_', s)
    s = re.sub('\+', '_', s)
    return s


def sanitize(s):
    s = s.split('-')[1]
    s = s.split('.')[0]
    return s


@cache.cached(timeout=default_cache_timeout, key_prefix='available_posts')
def create_post_cache():
    available_posts = []
    for post in os.listdir(POSTS_DIR):
        post_title = sanitize(post)
        with open(os.path.join(POSTS_DIR, post)) as f:
            _post_title = post_title
            post_title = re.sub('_', ' ', post_title)
            p_dict = {}
            p_dict['name'] = post_title
            p_content = f.read()
            post_data = p_content.split('\n')
            for line in post_data:
                if re.match('^#\ ', line):
                    p_dict['title'] = re.sub('#','', line).lstrip().rstrip()
                    break
            for line in post_data:
                if re.match('^##\ ', line):
                    p_dict['sub-title'] = re.sub('#', '', line).lstrip().rstrip()
                    break
            cache.set(_post_title, p_content, timeout=default_cache_timeout)

        available_posts.append(p_dict)

    return available_posts


def get_cached_item(post):
    u_post = unsanitize(post)
    rv = cache.get(u_post)

    if rv is None:
        app.logger.warn('{0} not found in cache'.format(u_post))
        posts = os.listdir(POSTS_DIR)
        for p in posts:
            if re.search(u_post + '\.', p):
                with open(os.path.join(POSTS_DIR, p)) as f:

                    _post_title = u_post
                    post_title = re.sub('_', ' ', u_post)
                    p_dict = {}
                    p_dict['name'] = post_title
                    p_content = f.read()
                    post_data = p_content.split('\n')
                    for line in post_data:
                        if re.match('^#\ ', line):
                            p_dict['title'] = re.sub('#', '', line).lstrip().rstrip()
                            break
                    for line in post_data:
                        if re.match('^##\ ', line):
                            p_dict['sub-title'] = re.sub('#', '', line).lstrip().rstrip()
                            break
                    cache.set(_post_title, p_content, timeout=default_cache_timeout)
                    return p_dict, p_content
            else:
                app.logger.warn('{0} not found.'.format(u_post))
                return None

    p_dict = {}
    post_title = re.sub('_', ' ', u_post)
    p_dict['name'] = post_title
    p_content = rv
    post_data = p_content.split('\n')
    for line in post_data:
        if re.match('^#\ ', line):
            p_dict['title'] = re.sub('#', '', line)
            break
    for line in post_data:
        if re.match('^##\ ', line):
            p_dict['sub-title'] = re.sub('#', '', line)
            break
    return p_dict, p_content

avail_posts = []
cached_posts = create_post_cache()

for p in reversed(cached_posts):
    avail_posts.append(p)


@app.route('/')
@cache.cached(timeout=default_cache_timeout)
def index():
    # only return latest 5 posts
    return render_template('index.html.j2',
                           posts=avail_posts[:5],
                           copy=COPYRIGHT,
                           blog_name=BLOG_NAME,
                           heading=BLOG_NAME,
                           sub_heading=SUB_HEADING)

@app.route('/about/')
@cache.cached(timeout=default_cache_timeout)
def about():
    with open(BASE_DIR + '/about.md') as f:
        content = f.read()
    if not content:
        content = ''
    content = Markup(markdown.markdown(content))
    return render_template('about.html.j2',
                           content=content,
                           copy=COPYRIGHT,
                           blog_name=BLOG_NAME,
                           heading=ABOUT_HEADING,
                           sub_heading=ABOUT_SUB)

@app.route('/posts/')
@cache.cached(timeout=default_cache_timeout)
def posts():
    return render_template('posts.html.j2',
                           posts=avail_posts,
                           copy=COPYRIGHT,
                           blog_name=BLOG_NAME,
                           heading=BLOG_NAME,
                           sub_heading=SUB_HEADING)


@app.route('/post/<post>')
@cache.cached(timeout=default_cache_timeout)
def post(post):
    post = unsanitize(post)

    try:
        meta, current_post = get_cached_item(post)
    except Exception:
        return page_not_found(404)
    current_post = re.sub('#\ *.*\n', '', current_post, count=1)
    current_post = re.sub('\n##\ *.*\n', '', current_post, count=1)
    post = Markup(markdown.markdown(current_post))
    if not 'title' in meta:
        meta['title'] = meta['name']

    if not 'sub-title' in meta:
        meta['sub-title'] = ''

    return render_template('post.html.j2',
                           post=post,
                           meta=meta,
                           copy=COPYRIGHT,
                           blog_name=BLOG_NAME,
                           heading=meta['title'],
                           sub_heading=meta['sub-title'])


@app.errorhandler(404)
@cache.cached(timeout=60)
def page_not_found(error):
    return render_template('posts.html.j2',
                           msg='Sorry, that blog post was not found. Please select a post from below.',
                           posts=avail_posts,
                           copy=COPYRIGHT,
                           heading=BLOG_NAME,
                           sub_heading=SUB_HEADING,
                           blog_name=BLOG_NAME), 404


if __name__ == '__main__':
    handler = logging.FileHandler(BASE_DIR + '/log/flask-blog.log')
    formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
    handler.setLevel(logging.WARN)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(debug=True)
