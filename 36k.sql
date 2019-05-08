CREATE TABLE `t_banner` (
`id` int NOT NULL AUTO_INCREMENT,
`name` varchar(32) NULL,
`url` varchar(128) NULL,
`sort` int(11) NULL,
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_article` (
`id` int NOT NULL AUTO_INCREMENT,
`title` varchar(128) NULL,
`cid` int(11) NULL,
`cover_pic` varchar(128) NULL,
`author_id` int(11) NULL,
`view_num` int(11) NULL DEFAULT 0,
`description` varchar(255) NULL,
`content` text NULL,
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_article_category` (
`id` int NOT NULL AUTO_INCREMENT,
`name` varchar(128) NULL,
`sort` int(11) NULL,
`content` text NULL,
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_article_praise` (
`id` int NOT NULL AUTO_INCREMENT,
`article_id` int(11) NULL,
`uid` int(11) NULL,
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_article_collet` (
`id` int NOT NULL AUTO_INCREMENT,
`article_id` int(11) NULL,
`uid` int(11) NULL,
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_customer` (
`id` int NOT NULL AUTO_INCREMENT,
`username` varchar(50) NULL,
`nickname` varchar(50) NULL,
`password` varchar(32) NULL,
`mobile` varchar(11) NULL,
`sex` int(1) NULL DEFAULT 0 COMMENT '0 女 1男',
`avatar` varchar(128) NULL,
`is_mobile_auth` int(1) NULL DEFAULT 0 COMMENT '0未验证 1验证',
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_article_comment` (
`id` int NOT NULL AUTO_INCREMENT,
`article_id` int(11) NULL,
`uid` int(11) NULL,
`content` text NULL,
`type` varchar(1) NULL DEFAULT '0' COMMENT '0评论 1回复',
`comment_id` int(11) NULL DEFAULT 0,
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_comment_praise` (
`id` int NOT NULL AUTO_INCREMENT,
`comment_id` int(11) NULL,
`uid` int(11) NULL,
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_mobile_code_record` (
`id` int NOT NULL AUTO_INCREMENT,
`ip` varchar(64) NULL,
`moblie` varchar(11) NULL,
`code` varchar(4) NULL,
`is_use` int(1) NULL DEFAULT 0 COMMENT '0未使用 1使用',
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `t_friend_link` (
`id` int NOT NULL AUTO_INCREMENT,
`name` varchar(64) NULL,
`link_type` int(1) NULL DEFAULT 0 COMMENT '0文本 1图标',
`link_icon` varchar(128) NULL,
`link_url` varchar(128) NULL DEFAULT '0' COMMENT '0未使用 1使用',
`sort` int(11) NULL,
`create_time` datetime NULL,
`update_time` datetime NULL,
PRIMARY KEY (`id`) 
);

