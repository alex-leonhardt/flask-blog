# Hello World!

<center>![image](/static/images/feedback_emoticon.png)</center>

## Welcome to the out-of-this-world blog!

So, surely you're wondering, why I did this ? Well, partially because I wanted a blog for myself. Partially to learn
more flasky goodness. 

### The idea

The idea was that I do not have to deal with Databases or the likes to create content, however, that once the app
starts, content will have to be cached so access to the data won't rely on the system's / host's IO. So I decided
to use Flask-Cache with its internal basic cache. You can utilize others like Redis and Memcache but I don't see
the need quite yet.

### The result

The result is this :) ! A simple blog applicaiton that can be run on anything python runs. You will need to install some
dependencies, all deps are in the ```requirements.txt```. I've also decided to use a existing bootstrap theme with 
close to no modifications to it. The source is here : <a href="https://github.com/IronSummitMedia/startbootstrap-clean-blog">https://github.com/IronSummitMedia/startbootstrap-clean-blog</a>

### New posts

New posts need to be placed into the ```posts/``` sub-directory - once that is done, you shoudl commit/push to your 
repo. You need to establish some mechanism to update the server you're running the blog from. I'd suggest to use 
either Ansible or a simple Fabric file to remotely manage your host(s).

Adding new posts will require a reload of the app unless you will wait for the cache to expire. Currently the cache is
by default set to **31 days**. Have a look at the settings details below, you can change ```default_cache_timeout```
to something smaller if you'd like to.

### Logging

Logging is set to WARNING level by default and logs will go into the relative path ```log/```. You should add a logrotate
file that will rotate and remove old logs. Logging has been made so it looks like JSON data - this should make it
easy to send the data to logstash or the likes if you'd like to. Currently only when a cache-miss was encountered
will we log "anything".

### Settings

There are several settings you should update within blog.py : 


    COPYRIGHT='MY_BLOG'
    BLOG_NAME='MY_BLOG'
    SUB_HEADING='A blog that\'s out of this world.'
    ABOUT_HEADING='About me'
    ABOUT_SUB='Just a another geek with another blog.'
    TWITTER_LINK=''
    FACEBOOK_LINK=''
    GITHUB_LINK=''
    default_cache_timeout = 2678400 # 31 days



