-- =============================================
-- 工时与项目协同管理系统 - PostgreSQL 数据库DDL
-- 文档版本：V1.0
-- 创建日期：2026-02-05
-- 适用于：PostgreSQL 15+
-- =============================================

-- 删除现有表（如果存在）- 按依赖关系倒序删除
DROP TABLE IF EXISTS work_task CASCADE;
DROP TABLE IF EXISTS report_template CASCADE;
DROP TABLE IF EXISTS sys_message CASCADE;
DROP TABLE IF EXISTS work_problem CASCADE;
DROP TABLE IF EXISTS annual_plan CASCADE;
DROP TABLE IF EXISTS project_statistic CASCADE;
DROP TABLE IF EXISTS project_info CASCADE;
DROP TABLE IF EXISTS work_daily CASCADE;
DROP TABLE IF EXISTS sys_user_role_permission CASCADE;
DROP TABLE IF EXISTS sys_menu CASCADE;
DROP TABLE IF EXISTS sys_permission_code CASCADE;
DROP TABLE IF EXISTS sys_timezone CASCADE;
DROP TABLE IF EXISTS sys_role CASCADE;
DROP TABLE IF EXISTS sys_user CASCADE;
DROP TABLE IF EXISTS sys_department CASCADE;

-- =============================================
-- 1. 部门表 (sys_department) - 基础表，无外键依赖
-- =============================================
CREATE TABLE sys_department (
    id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    dept_code VARCHAR(50) UNIQUE NOT NULL,
    parent_id INT,
    dept_level INT DEFAULT 1,
    dept_desc TEXT,
    manager_id INT,
    sort_order INT DEFAULT 0,
    status SMALLINT DEFAULT 1,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES sys_department(id) ON DELETE SET NULL
);

COMMENT ON TABLE sys_department IS '系统部门表';
COMMENT ON COLUMN sys_department.dept_name IS '部门名称';
COMMENT ON COLUMN sys_department.dept_code IS '部门编码';
COMMENT ON COLUMN sys_department.parent_id IS '上级部门ID，自关联';
COMMENT ON COLUMN sys_department.dept_level IS '部门层级';
COMMENT ON COLUMN sys_department.dept_desc IS '部门描述';
COMMENT ON COLUMN sys_department.manager_id IS '部门负责人ID';
COMMENT ON COLUMN sys_department.sort_order IS '排序序号';
COMMENT ON COLUMN sys_department.status IS '部门状态：1-启用，0-禁用';

-- =============================================
-- 2. 角色权限表 (sys_role) - 基础表，无外键依赖
-- =============================================
CREATE TABLE sys_role (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL,
    role_code VARCHAR(50) UNIQUE NOT NULL,
    role_desc TEXT,
    permissions JSONB,
    data_scope VARCHAR(20) DEFAULT 'personal',
    status SMALLINT DEFAULT 1,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE sys_role IS '系统角色权限表';
COMMENT ON COLUMN sys_role.role_name IS '角色名称';
COMMENT ON COLUMN sys_role.role_code IS '角色编码';
COMMENT ON COLUMN sys_role.role_desc IS '角色描述';
COMMENT ON COLUMN sys_role.permissions IS '权限配置JSON';
COMMENT ON COLUMN sys_role.data_scope IS '数据权限范围：personal-个人，team-团队，department-部门，company-公司';
COMMENT ON COLUMN sys_role.status IS '角色状态：1-启用，0-禁用';

-- =============================================
-- 3. 用户表 (sys_user) - 依赖部门表和角色表
-- =============================================
CREATE TABLE sys_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    real_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    dept_id INT,
    position VARCHAR(100),
    role_id INT,
    status SMALLINT DEFAULT 1,
    last_login TIMESTAMP,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES sys_department(id) ON DELETE SET NULL,
    FOREIGN KEY (role_id) REFERENCES sys_role(id) ON DELETE SET NULL
);

COMMENT ON TABLE sys_user IS '系统用户表';
COMMENT ON COLUMN sys_user.username IS '登录账号';
COMMENT ON COLUMN sys_user.password IS '加密密码';
COMMENT ON COLUMN sys_user.real_name IS '真实姓名';
COMMENT ON COLUMN sys_user.email IS '邮箱地址';
COMMENT ON COLUMN sys_user.phone IS '手机号码';
COMMENT ON COLUMN sys_user.dept_id IS '所属部门ID，关联sys_department表';
COMMENT ON COLUMN sys_user.position IS '职位';
COMMENT ON COLUMN sys_user.role_id IS '角色ID，关联sys_role表';
COMMENT ON COLUMN sys_user.status IS '账号状态：1-启用，0-禁用';
COMMENT ON COLUMN sys_user.last_login IS '最后登录时间';
COMMENT ON COLUMN sys_user.create_time IS '创建时间';
COMMENT ON COLUMN sys_user.update_time IS '更新时间';

-- =============================================
-- 4. 更新部门表，添加用户外键约束
-- =============================================
ALTER TABLE sys_department ADD CONSTRAINT fk_department_manager 
    FOREIGN KEY (manager_id) REFERENCES sys_user(id) ON DELETE SET NULL;

-- =============================================
-- 5. 权限码表 (sys_permission_code) - 基础表
-- =============================================
CREATE TABLE sys_permission_code (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    resource_type VARCHAR(20) DEFAULT 'menu',
    status SMALLINT DEFAULT 1,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE sys_permission_code IS '系统权限码表';
COMMENT ON COLUMN sys_permission_code.code IS '权限编码';
COMMENT ON COLUMN sys_permission_code.name IS '权限名称';
COMMENT ON COLUMN sys_permission_code.description IS '权限描述';
COMMENT ON COLUMN sys_permission_code.resource_type IS '资源类型：menu-菜单，button-按钮，api-api接口';
COMMENT ON COLUMN sys_permission_code.status IS '状态：1-启用，0-禁用';

-- =============================================
-- 6. 菜单表 (sys_menu) - 基础表，自关联
-- =============================================
CREATE TABLE sys_menu (
    id SERIAL PRIMARY KEY,
    pid INT,
    name VARCHAR(100) NOT NULL,
    path VARCHAR(200),
    component VARCHAR(200),
    redirect VARCHAR(200),
    meta JSONB,
    icon VARCHAR(50),
    type VARCHAR(20) DEFAULT 'menu',
    status SMALLINT DEFAULT 1,
    sort_order INT DEFAULT 0,
    auth_code VARCHAR(50),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pid) REFERENCES sys_menu(id) ON DELETE CASCADE
);

COMMENT ON TABLE sys_menu IS '系统菜单表';
COMMENT ON COLUMN sys_menu.pid IS '父级菜单ID，自关联';
COMMENT ON COLUMN sys_menu.name IS '菜单名称';
COMMENT ON COLUMN sys_menu.path IS '路由路径';
COMMENT ON COLUMN sys_menu.component IS '组件路径';
COMMENT ON COLUMN sys_menu.redirect IS '重定向路径';
COMMENT ON COLUMN sys_menu.meta IS '菜单元信息';
COMMENT ON COLUMN sys_menu.icon IS '图标';
COMMENT ON COLUMN sys_menu.type IS '菜单类型：catalog-目录，menu-菜单，button-按钮，link-外链，embedded-内嵌';
COMMENT ON COLUMN sys_menu.status IS '状态：1-启用，0-禁用';
COMMENT ON COLUMN sys_menu.sort_order IS '排序序号';
COMMENT ON COLUMN sys_menu.auth_code IS '权限编码';

-- =============================================
-- 7. 用户角色权限表 (sys_user_role_permission) - 关联表
-- =============================================
CREATE TABLE sys_user_role_permission (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    role_code VARCHAR(50) NOT NULL,
    permission_codes JSONB,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
);

COMMENT ON TABLE sys_user_role_permission IS '用户角色权限关联表';
COMMENT ON COLUMN sys_user_role_permission.user_id IS '用户ID';
COMMENT ON COLUMN sys_user_role_permission.role_code IS '角色编码';
COMMENT ON COLUMN sys_user_role_permission.permission_codes IS '权限编码列表';

-- =============================================
-- 8. 时区表 (sys_timezone) - 基础表
-- =============================================
CREATE TABLE sys_timezone (
    id SERIAL PRIMARY KEY,
    timezone VARCHAR(50) UNIQUE NOT NULL,
    "offset" INT NOT NULL,
    display_name VARCHAR(100),
    country_code VARCHAR(10),
    status SMALLINT DEFAULT 1,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE sys_timezone IS '系统时区表';
COMMENT ON COLUMN sys_timezone.timezone IS '时区标识';
COMMENT ON COLUMN sys_timezone."offset" IS '时区偏移（小时）';
COMMENT ON COLUMN sys_timezone.display_name IS '显示名称';
COMMENT ON COLUMN sys_timezone.country_code IS '国家代码';
COMMENT ON COLUMN sys_timezone.status IS '状态：1-启用，0-禁用';

-- =============================================
-- 9. 每日工作填报表 (work_daily) - 依赖用户表
-- =============================================
CREATE TABLE work_daily (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    work_date DATE NOT NULL,
    project_id INT,
    project_name VARCHAR(200),
    work_content TEXT NOT NULL,
    difficulty VARCHAR(20),
    urgency VARCHAR(20),
    work_type VARCHAR(50),
    planned_hours NUMERIC(5,1),
    actual_hours NUMERIC(5,1) NOT NULL,
    interference TEXT,
    remark TEXT,
    status SMALLINT DEFAULT 1,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
);

COMMENT ON TABLE work_daily IS '每日工作填报表';
COMMENT ON COLUMN work_daily.user_id IS '用户ID';
COMMENT ON COLUMN work_daily.work_date IS '工作日期';
COMMENT ON COLUMN work_daily.project_id IS '项目ID，关联project_info表';
COMMENT ON COLUMN work_daily.project_name IS '项目名称';
COMMENT ON COLUMN work_daily.work_content IS '工作内容';
COMMENT ON COLUMN work_daily.difficulty IS '难度等级：easy-简单，normal-一般，hard-困难';
COMMENT ON COLUMN work_daily.urgency IS '紧急程度：low-低，medium-中，high-高';
COMMENT ON COLUMN work_daily.work_type IS '工作类型：development-开发，test-测试，design-设计，meeting-会议等';
COMMENT ON COLUMN work_daily.planned_hours IS '计划工时';
COMMENT ON COLUMN work_daily.actual_hours IS '实际工时';
COMMENT ON COLUMN work_daily.interference IS '干扰因素';
COMMENT ON COLUMN work_daily.remark IS '备注说明';
COMMENT ON COLUMN work_daily.status IS '状态：1-正常，0-删除';

-- =============================================
-- 10. 项目基础信息表 (project_info) - 依赖用户表
-- =============================================
CREATE TABLE project_info (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(200) UNIQUE NOT NULL,
    project_code VARCHAR(50) UNIQUE,
    description TEXT,
    local_path TEXT,
    online_url TEXT,
    svn_url TEXT,
    git_url TEXT,
    node_version VARCHAR(20),
    python_version VARCHAR(20),
    java_version VARCHAR(20),
    database_type VARCHAR(50),
    leader_id INT,
    team_members JSONB,
    start_date DATE,
    end_date DATE,
    actual_end_date DATE,
    project_status VARCHAR(20) DEFAULT 'planning',
    priority VARCHAR(20) DEFAULT 'medium',
    budget DECIMAL(12,2),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (leader_id) REFERENCES sys_user(id) ON DELETE SET NULL
);

COMMENT ON TABLE project_info IS '项目基础信息表';
COMMENT ON COLUMN project_info.project_name IS '项目名称';
COMMENT ON COLUMN project_info.project_code IS '项目编码';
COMMENT ON COLUMN project_info.description IS '项目描述';
COMMENT ON COLUMN project_info.local_path IS '本地路径';
COMMENT ON COLUMN project_info.online_url IS '线上地址';
COMMENT ON COLUMN project_info.svn_url IS 'SVN地址';
COMMENT ON COLUMN project_info.git_url IS 'Git仓库地址';
COMMENT ON COLUMN project_info.node_version IS 'Node版本要求';
COMMENT ON COLUMN project_info.python_version IS 'Python版本要求';
COMMENT ON COLUMN project_info.java_version IS 'Java版本要求';
COMMENT ON COLUMN project_info.database_type IS '数据库类型';
COMMENT ON COLUMN project_info.leader_id IS '项目负责人ID';
COMMENT ON COLUMN project_info.team_members IS '团队成员ID数组';
COMMENT ON COLUMN project_info.start_date IS '开始日期';
COMMENT ON COLUMN project_info.end_date IS '预计结束日期';
COMMENT ON COLUMN project_info.actual_end_date IS '实际结束日期';
COMMENT ON COLUMN project_info.project_status IS '项目状态：planning-规划中，in_progress-进行中，testing-测试中，completed-已完成，cancelled-已取消';
COMMENT ON COLUMN project_info.priority IS '优先级：low-低，medium-中，high-高，urgent-紧急';
COMMENT ON COLUMN project_info.budget IS '项目预算';

-- =============================================
-- 11. 项目统计表 (project_statistic) - 依赖项目表
-- =============================================
CREATE TABLE project_statistic (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    leader_name VARCHAR(50),
    total_hours NUMERIC(10,1) DEFAULT 0,
    develop_cycle INT DEFAULT 0,
    bug_count INT DEFAULT 0,
    feature_count INT DEFAULT 0,
    requirement_count INT DEFAULT 0,
    project_status VARCHAR(20),
    delivery_quality VARCHAR(20),
    satisfaction_score DECIMAL(3,1),
    risk_level VARCHAR(20) DEFAULT 'low',
    last_update_date DATE,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project_info(id) ON DELETE CASCADE
);

COMMENT ON TABLE project_statistic IS '项目统计表';
COMMENT ON COLUMN project_statistic.project_id IS '项目ID';
COMMENT ON COLUMN project_statistic.leader_name IS '项目负责人姓名';
COMMENT ON COLUMN project_statistic.total_hours IS '项目累计工时';
COMMENT ON COLUMN project_statistic.develop_cycle IS '开发周期（天）';
COMMENT ON COLUMN project_statistic.bug_count IS 'BUG修复次数';
COMMENT ON COLUMN project_statistic.feature_count IS '功能点数量';
COMMENT ON COLUMN project_statistic.requirement_count IS '需求数量';
COMMENT ON COLUMN project_statistic.project_status IS '项目状态';
COMMENT ON COLUMN project_statistic.delivery_quality IS '交付质量评级：excellent-优秀，good-良好，normal-一般，poor-较差';
COMMENT ON COLUMN project_statistic.satisfaction_score IS '满意度评分（1-10分）';
COMMENT ON COLUMN project_statistic.risk_level IS '风险等级：low-低，medium-中，high-高';
COMMENT ON COLUMN project_statistic.last_update_date IS '最后更新日期';

-- =============================================
-- 12. 年度计划表 (annual_plan) - 依赖用户表
-- =============================================
CREATE TABLE annual_plan (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    plan_content TEXT NOT NULL,
    target TEXT,
    result TEXT,
    completion_status VARCHAR(20) DEFAULT 'pending',
    difficulty VARCHAR(20),
    document_url TEXT,
    risk_remark TEXT,
    start_date DATE,
    end_date DATE,
    actual_completion_date DATE,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
);

COMMENT ON TABLE annual_plan IS '年度计划表';
COMMENT ON COLUMN annual_plan.user_id IS '用户ID';
COMMENT ON COLUMN annual_plan.year IS '年份';
COMMENT ON COLUMN annual_plan.month IS '月份（1-12）';
COMMENT ON COLUMN annual_plan.plan_content IS '计划内容';
COMMENT ON COLUMN annual_plan.target IS '目标要求';
COMMENT ON COLUMN annual_plan.result IS '实际结果';
COMMENT ON COLUMN annual_plan.completion_status IS '完成状态：pending-待完成，in_progress-进行中，completed-已完成，delayed-已延期';
COMMENT ON COLUMN annual_plan.difficulty IS '难度等级：easy-简单，normal-一般，hard-困难';
COMMENT ON COLUMN annual_plan.document_url IS '相关文档链接';
COMMENT ON COLUMN annual_plan.risk_remark IS '风险备注';
COMMENT ON COLUMN annual_plan.start_date IS '计划开始日期';
COMMENT ON COLUMN annual_plan.end_date IS '计划结束日期';
COMMENT ON COLUMN annual_plan.actual_completion_date IS '实际完成日期';

-- =============================================
-- 13. 工作问题复盘表 (work_problem) - 依赖用户表
-- =============================================
CREATE TABLE work_problem (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    year INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    core_problem TEXT NOT NULL,
    root_cause TEXT,
    rectify_measure TEXT,
    effect_assessment TEXT,
    quantified_target TEXT,
    actual_effect TEXT,
    improvement_status VARCHAR(20) DEFAULT 'open',
    follow_up_person VARCHAR(50),
    resolution_date DATE,
    remark TEXT,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
);

COMMENT ON TABLE work_problem IS '工作问题复盘表';
COMMENT ON COLUMN work_problem.user_id IS '用户ID';
COMMENT ON COLUMN work_problem.year IS '年份';
COMMENT ON COLUMN work_problem.category IS '问题分类：technical-技术问题，process-流程问题，communication-沟通问题，other-其他';
COMMENT ON COLUMN work_problem.core_problem IS '核心问题描述';
COMMENT ON COLUMN work_problem.root_cause IS '根本原因分析';
COMMENT ON COLUMN work_problem.rectify_measure IS '整改措施';
COMMENT ON COLUMN work_problem.effect_assessment IS '效果评估';
COMMENT ON COLUMN work_problem.quantified_target IS '量化目标';
COMMENT ON COLUMN work_problem.actual_effect IS '实际效果';
COMMENT ON COLUMN work_problem.improvement_status IS '改进状态：open-待处理，in_progress-处理中，resolved-已解决，closed-已关闭';
COMMENT ON COLUMN work_problem.follow_up_person IS '跟进人';
COMMENT ON COLUMN work_problem.resolution_date IS '解决日期';
COMMENT ON COLUMN work_problem.remark IS '备注说明';

-- =============================================
-- 14. 消息通知表 (sys_message) - 依赖用户表
-- =============================================
CREATE TABLE sys_message (
    id SERIAL PRIMARY KEY,
    sender_id INT,
    receiver_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    msg_type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal',
    is_read SMALLINT DEFAULT 0,
    read_time TIMESTAMP,
    related_id INT,
    related_type VARCHAR(50),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES sys_user(id) ON DELETE SET NULL,
    FOREIGN KEY (receiver_id) REFERENCES sys_user(id) ON DELETE CASCADE
);

COMMENT ON TABLE sys_message IS '系统消息通知表';
COMMENT ON COLUMN sys_message.sender_id IS '发送者ID';
COMMENT ON COLUMN sys_message.receiver_id IS '接收者ID';
COMMENT ON COLUMN sys_message.title IS '消息标题';
COMMENT ON COLUMN sys_message.content IS '消息内容';
COMMENT ON COLUMN sys_message.msg_type IS '消息类型：daily_remind-日报提醒，plan_remind-计划提醒，task_assign-任务指派，system_notice-系统通知';
COMMENT ON COLUMN sys_message.priority IS '优先级：low-低，normal-普通，high-高，urgent-紧急';
COMMENT ON COLUMN sys_message.is_read IS '是否已读：0-未读，1-已读';
COMMENT ON COLUMN sys_message.read_time IS '阅读时间';
COMMENT ON COLUMN sys_message.related_id IS '关联业务ID（如任务ID、计划ID等）';
COMMENT ON COLUMN sys_message.related_type IS '关联业务类型';

-- =============================================
-- 15. 报告模板表 (report_template) - 基础表，无外键依赖
-- =============================================
CREATE TABLE report_template (
    id SERIAL PRIMARY KEY,
    template_name VARCHAR(100) NOT NULL,
    dept VARCHAR(50),
    role VARCHAR(50),
    template_type VARCHAR(20) NOT NULL,
    content JSONB NOT NULL,
    file_path TEXT,
    preview_image TEXT,
    is_default SMALLINT DEFAULT 0,
    status SMALLINT DEFAULT 1,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE report_template IS '报告模板表';
COMMENT ON COLUMN report_template.template_name IS '模板名称';
COMMENT ON COLUMN report_template.dept IS '适用部门';
COMMENT ON COLUMN report_template.role IS '适用角色';
COMMENT ON COLUMN report_template.template_type IS '模板类型：ppt-pptx，pdf-pdf，word-docx，excel-xlsx';
COMMENT ON COLUMN report_template.content IS '模板内容配置';
COMMENT ON COLUMN report_template.file_path IS '模板文件路径';
COMMENT ON COLUMN report_template.preview_image IS '预览图片路径';
COMMENT ON COLUMN report_template.is_default IS '是否默认模板：0-否，1-是';
COMMENT ON COLUMN report_template.status IS '模板状态：1-启用，0-禁用';

-- =============================================
-- 16. 任务下发表 (work_task) - 依赖用户表
-- =============================================
CREATE TABLE work_task (
    id SERIAL PRIMARY KEY,
    publisher_id INT NOT NULL,
    receiver_id INT NOT NULL,
    task_content TEXT NOT NULL,
    task_type VARCHAR(50) DEFAULT 'general',
    priority VARCHAR(20) DEFAULT 'medium',
    deadline DATE NOT NULL,
    estimated_hours NUMERIC(5,1),
    actual_hours NUMERIC(5,1),
    status VARCHAR(20) DEFAULT 'assigned',
    completion_description TEXT,
    attachment_urls JSONB,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_time TIMESTAMP,
    FOREIGN KEY (publisher_id) REFERENCES sys_user(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES sys_user(id) ON DELETE CASCADE
);

COMMENT ON TABLE work_task IS '工作任务下发表';
COMMENT ON COLUMN work_task.publisher_id IS '发布者ID';
COMMENT ON COLUMN work_task.receiver_id IS '接收者ID';
COMMENT ON COLUMN work_task.task_content IS '任务内容';
COMMENT ON COLUMN work_task.task_type IS '任务类型：general-一般任务，urgent-紧急任务，review-审核任务';
COMMENT ON COLUMN work_task.priority IS '优先级：low-低，medium-中，high-高，urgent-紧急';
COMMENT ON COLUMN work_task.deadline IS '截止日期';
COMMENT ON COLUMN work_task.estimated_hours IS '预估工时';
COMMENT ON COLUMN work_task.actual_hours IS '实际工时';
COMMENT ON COLUMN work_task.status IS '任务状态：assigned-已指派，in_progress-进行中，completed-已完成，rejected-已拒绝，expired-已过期';
COMMENT ON COLUMN work_task.completion_description IS '完成情况描述';
COMMENT ON COLUMN work_task.attachment_urls IS '附件URL数组';
COMMENT ON COLUMN work_task.completed_time IS '完成时间';

-- =============================================
-- 创建索引以提升查询性能
-- =============================================

-- 用户相关索引
CREATE INDEX idx_sys_user_username ON sys_user(username);
CREATE INDEX idx_sys_user_email ON sys_user(email);
CREATE INDEX idx_sys_user_dept_id ON sys_user(dept_id);
CREATE INDEX idx_sys_user_role_id ON sys_user(role_id);

-- 部门相关索引
CREATE INDEX idx_sys_department_code ON sys_department(dept_code);
CREATE INDEX idx_sys_department_parent ON sys_department(parent_id);
CREATE INDEX idx_sys_department_manager ON sys_department(manager_id);

-- 权限相关索引
CREATE INDEX idx_sys_permission_code ON sys_permission_code(code);
CREATE INDEX idx_sys_permission_resource ON sys_permission_code(resource_type);

-- 菜单相关索引
CREATE INDEX idx_sys_menu_pid ON sys_menu(pid);
CREATE INDEX idx_sys_menu_type ON sys_menu(type);
CREATE INDEX idx_sys_menu_auth_code ON sys_menu(auth_code);

-- 用户权限相关索引
CREATE INDEX idx_sys_user_role_perm_user ON sys_user_role_permission(user_id);
CREATE INDEX idx_sys_user_role_perm_role ON sys_user_role_permission(role_code);

-- 时区相关索引
CREATE INDEX idx_sys_timezone_offset ON sys_timezone("offset");
CREATE INDEX idx_sys_timezone_country ON sys_timezone(country_code);

-- 工作填报相关索引
CREATE INDEX idx_work_daily_user_date ON work_daily(user_id, work_date);
CREATE INDEX idx_work_daily_project ON work_daily(project_id);
CREATE INDEX idx_work_daily_work_date ON work_daily(work_date);
CREATE INDEX idx_work_daily_status ON work_daily(status);

-- 项目相关索引
CREATE INDEX idx_project_info_leader ON project_info(leader_id);
CREATE INDEX idx_project_info_status ON project_info(project_status);
CREATE INDEX idx_project_info_priority ON project_info(priority);
CREATE INDEX idx_project_statistic_project ON project_statistic(project_id);

-- 计划相关索引
CREATE INDEX idx_annual_plan_user_year ON annual_plan(user_id, year);
CREATE INDEX idx_annual_plan_year_month ON annual_plan(year, month);
CREATE INDEX idx_annual_plan_status ON annual_plan(completion_status);

-- 问题复盘相关索引
CREATE INDEX idx_work_problem_user_year ON work_problem(user_id, year);
CREATE INDEX idx_work_problem_category ON work_problem(category);
CREATE INDEX idx_work_problem_status ON work_problem(improvement_status);

-- 消息通知相关索引
CREATE INDEX idx_sys_message_receiver ON sys_message(receiver_id);
CREATE INDEX idx_sys_message_type ON sys_message(msg_type);
CREATE INDEX idx_sys_message_is_read ON sys_message(is_read);
CREATE INDEX idx_sys_message_create_time ON sys_message(create_time);

-- 任务相关索引
CREATE INDEX idx_work_task_publisher ON work_task(publisher_id);
CREATE INDEX idx_work_task_receiver ON work_task(receiver_id);
CREATE INDEX idx_work_task_deadline ON work_task(deadline);
CREATE INDEX idx_work_task_status ON work_task(status);

-- =============================================
-- 插入初始数据
-- =============================================

-- 插入默认部门
INSERT INTO sys_department (dept_name, dept_code, dept_desc, sort_order) VALUES
('技术部', 'TECH', '技术研发部门', 1),
('产品部', 'PRODUCT', '产品设计部门', 2),
('运营部', 'OPERATION', '运营管理部门', 3),
('人事部', 'HR', '人力资源部门', 4);

-- 插入默认角色
INSERT INTO sys_role (role_name, role_code, role_desc, permissions, data_scope) VALUES
('超级管理员', 'admin', '系统超级管理员，拥有全部权限', '{"*": "*"}', 'company'),
('项目总监', 'project_director', '项目总监，可查看所有项目数据', '{"project": "*", "report": "*"}', 'company'),
('部门经理', 'dept_manager', '部门经理，可查看部门内所有数据', '{"project": "department", "report": "department"}', 'department'),
('技术经理', 'tech_manager', '技术经理，负责技术团队管理', '{"project": "team", "problem": "team"}', 'team'),
('项目经理', 'project_manager', '项目经理，负责具体项目管理', '{"project": "personal", "task": "team"}', 'team'),
('普通员工', 'employee', '普通员工，只能查看个人数据', '{"worklog": "personal", "plan": "personal"}', 'personal');

-- 插入默认管理员用户（密码将在后续脚本中加密）
INSERT INTO sys_user (username, password, real_name, email, dept_id, role_id, status) VALUES
('admin', 'admin123', '系统管理员', 'admin@example.com', 1, 1, 1);

-- 插入其他测试用户（密码将在后续脚本中加密）
INSERT INTO sys_user (username, password, real_name, email, dept_id, role_id, status) VALUES
('zhangsan', 'zhangsan123', '张三', 'zhangsan@example.com', 1, 2, 1),
('lisi', 'lisi123', '李四', 'lisi@example.com', 1, 3, 1),
('wangwu', 'wangwu123', '王五', 'wangwu@example.com', 2, 4, 1),
('zhaoliu', 'zhaoliu123', '赵六', 'zhaoliu@example.com', 3, 5, 1),
('sunqi', 'sunqi123', '孙七', 'sunqi@example.com', 1, 6, 1);

-- 建议：在首次运行时，通过API或管理界面重置管理员密码

-- 插入默认报告模板
INSERT INTO report_template (template_name, dept, role, template_type, content, is_default, status) VALUES
('通用日报模板', 'all', 'all', 'word', '{"sections": ["工作内容", "遇到问题", "明日计划"]}', 1, 1),
('项目周报模板', 'tech', 'project_manager', 'ppt', '{"slides": ["项目进度", "本周成果", "下周计划", "风险预警"]}', 1, 1),
('部门月报模板', 'all', 'dept_manager', 'excel', '{"sheets": ["工时统计", "项目进度", "人员效能"]}', 1, 1);

-- =============================================
-- 创建更新时间自动更新函数
-- =============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $func$
BEGIN
    NEW.update_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$func$ LANGUAGE plpgsql;

-- 为所有表创建更新时间触发器
CREATE TRIGGER update_sys_user_updated_at BEFORE UPDATE ON sys_user FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sys_department_updated_at BEFORE UPDATE ON sys_department FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sys_role_updated_at BEFORE UPDATE ON sys_role FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sys_permission_code_updated_at BEFORE UPDATE ON sys_permission_code FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sys_menu_updated_at BEFORE UPDATE ON sys_menu FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sys_user_role_permission_updated_at BEFORE UPDATE ON sys_user_role_permission FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sys_timezone_updated_at BEFORE UPDATE ON sys_timezone FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_work_daily_updated_at BEFORE UPDATE ON work_daily FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_project_info_updated_at BEFORE UPDATE ON project_info FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_project_statistic_updated_at BEFORE UPDATE ON project_statistic FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_annual_plan_updated_at BEFORE UPDATE ON annual_plan FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_work_problem_updated_at BEFORE UPDATE ON work_problem FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sys_message_updated_at BEFORE UPDATE ON sys_message FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_report_template_updated_at BEFORE UPDATE ON report_template FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_work_task_updated_at BEFORE UPDATE ON work_task FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- 数据库初始化完成
-- =============================================
SELECT '数据库表结构创建完成！' as message;
SELECT '默认管理员账号：admin/admin123' as message;
SELECT '请根据实际需求调整初始数据和权限配置' as message;
