-- 408 考研信息聚合平台 MySQL 数据库表结构设计
-- 编码：UTF-8
-- 引擎：InnoDB

CREATE DATABASE IF NOT EXISTS `grad_info_408` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `grad_info_408`;

-- ==========================================
-- 1. 院校表 (institutions)
-- 记录全国开设 408 统考相关专业的高校信息
-- ==========================================
CREATE TABLE IF NOT EXISTS `institutions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `school_code` VARCHAR(20) NOT NULL UNIQUE COMMENT '院校代码 (如: 10001)',
    `name` VARCHAR(100) NOT NULL COMMENT '院校名称 (如: 北京大学)',
    `province` VARCHAR(50) NOT NULL COMMENT '所在省份 (如: 北京)',
    `city` VARCHAR(50) DEFAULT NULL COMMENT '所在城市',
    `is_985` BOOLEAN DEFAULT FALSE COMMENT '是否985',
    `is_211` BOOLEAN DEFAULT FALSE COMMENT '是否211',
    `is_double_first_class` BOOLEAN DEFAULT FALSE COMMENT '是否双一流',
    `official_website` VARCHAR(255) DEFAULT NULL COMMENT '学校官网地址',
    `grad_website` VARCHAR(255) DEFAULT NULL COMMENT '研究生院官网地址',
    `description` TEXT DEFAULT NULL COMMENT '院校简介',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_province` (`province`),
    INDEX `idx_name` (`name`)
) ENGINE=InnoDB COMMENT='院校信息表';

-- ==========================================
-- 2. 招生专业/学院表 (majors)
-- 记录具体学院及开考 408 的专业信息 (例如：计算机科学与技术、软件工程)
-- ==========================================
CREATE TABLE IF NOT EXISTS `majors` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `institution_id` INT NOT NULL COMMENT '关联的院校ID',
    `college_name` VARCHAR(100) NOT NULL COMMENT '招生院系名称 (如: 计算机学院)',
    `major_code` VARCHAR(20) NOT NULL COMMENT '专业代码 (如: 081200)',
    `major_name` VARCHAR(100) NOT NULL COMMENT '专业名称 (如: 计算机科学与技术)',
    `degree_type` ENUM('academic', 'professional') NOT NULL COMMENT '学位类型 (academic:学硕, professional:专硕)',
    `study_mode` ENUM('full_time', 'part_time') NOT NULL DEFAULT 'full_time' COMMENT '学习方式 (全日制/非全日制)',
    `exam_subjects` VARCHAR(255) NOT NULL COMMENT '考试科目(JSON/逗号分隔) 需包含: 101思想政治理论,201英语一,301数学一,408计算机学科专业基础综合',
    `research_directions` TEXT DEFAULT NULL COMMENT '研究方向 (JSON/换行符分隔)',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`institution_id`) REFERENCES `institutions`(`id`) ON DELETE CASCADE,
    INDEX `idx_major_code` (`major_code`)
) ENGINE=InnoDB COMMENT='招生专业信息表';

-- ==========================================
-- 3. 招生计划/简章信息表 (admission_plans)
-- 记录具体某一年某个专业的拟招生人数、推免人数等
-- ==========================================
CREATE TABLE IF NOT EXISTS `admission_plans` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `major_id` INT NOT NULL COMMENT '关联的专业ID',
    `year` YEAR NOT NULL COMMENT '招生年份 (如: 2025)',
    `total_plan` INT DEFAULT 0 COMMENT '拟招总人数',
    `exempt_plan` INT DEFAULT 0 COMMENT '拟接收推免人数',
    `unified_plan` INT DEFAULT 0 COMMENT '拟统招人数 (总人数 - 推免)',
    `tuition_fee` VARCHAR(100) DEFAULT NULL COMMENT '学费标准 (如: 8000元/年)',
    `schooling_length` VARCHAR(50) DEFAULT NULL COMMENT '学制 (如: 3年, 2.5年)',
    `remarks` TEXT DEFAULT NULL COMMENT '备注(特殊要求/跨考加试等)',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`major_id`) REFERENCES `majors`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_major_year` (`major_id`, `year`)
) ENGINE=InnoDB COMMENT='年度招生计划表';

-- ==========================================
-- 4. 历年分数线与报录比 (historical_data)
-- 记录复试线、录取均分、报录比等核心参考数据
-- ==========================================
CREATE TABLE IF NOT EXISTS `historical_data` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `major_id` INT NOT NULL COMMENT '关联的专业ID',
    `year` YEAR NOT NULL COMMENT '数据年份',
    `political_line` INT DEFAULT NULL COMMENT '政治单科线',
    `english_line` INT DEFAULT NULL COMMENT '英语单科线',
    `math_line` INT DEFAULT NULL COMMENT '数学单科线',
    `professional_line` INT DEFAULT NULL COMMENT '专业课(408)单科线',
    `total_score_line` INT DEFAULT NULL COMMENT '复试总分线/院线',
    `highest_score` INT DEFAULT NULL COMMENT '录取最高分',
    `lowest_score` INT DEFAULT NULL COMMENT '录取最低分',
    `average_score` DECIMAL(5,2) DEFAULT NULL COMMENT '录取平均分',
    `applicants_count` INT DEFAULT NULL COMMENT '报考人数',
    `admitted_count` INT DEFAULT NULL COMMENT '实际录取人数',
    `ratio` DECIMAL(5,2) DEFAULT NULL COMMENT '报录比 (报考/录取)',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`major_id`) REFERENCES `majors`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `uk_major_year` (`major_id`, `year`)
) ENGINE=InnoDB COMMENT='历年分数线与录取数据表';

-- ==========================================
-- 5. 官方通知公告 (official_notices)
-- 记录高校研究生院或研招网发布的各类通知 (简章、调剂、复试、拟录取等)
-- ==========================================
CREATE TABLE IF NOT EXISTS `official_notices` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `institution_id` INT DEFAULT NULL COMMENT '关联的院校ID (若为全国通用通知则为NULL)',
    `title` VARCHAR(255) NOT NULL COMMENT '通知标题',
    `url` VARCHAR(500) NOT NULL COMMENT '原文链接',
    `source` VARCHAR(100) NOT NULL COMMENT '来源 (如: 研招网, XX大学研究生院)',
    `category` ENUM('admission_guide', 'adjustment', 'retest', 'admission_list', 'other') NOT NULL DEFAULT 'other' COMMENT '通知分类 (简章/调剂/复试/拟录取/其他)',
    `publish_date` DATE NOT NULL COMMENT '发布日期',
    `content_summary` TEXT DEFAULT NULL COMMENT '内容摘要/抓取的正文',
    `is_parsed` BOOLEAN DEFAULT FALSE COMMENT '是否已被系统解析提取结构化数据',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`institution_id`) REFERENCES `institutions`(`id`) ON DELETE SET NULL,
    INDEX `idx_publish_date` (`publish_date`),
    INDEX `idx_category` (`category`)
) ENGINE=InnoDB COMMENT='官方招生通知公告表';
