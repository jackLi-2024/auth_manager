### 说明：
    1.框架运行
        本地运行: python3 lambda_function.py
        物理机部署: sh bin/start.sh
        aws-serverless运行: 入口为lambda_function.lambda_handler
    2.开发者需知
        开发者只需要在module下定义自己的功能模块
        例如实例中给出了test模块
            a.api.py  定义接口模型
            b.model.py 定义数据接口模型
            c.deal.py 逻辑处理函数
            
            # 备注（重要）:开发者可以按文档全部调试自己的代码，也可以仅仅定义自己业务模块（例如test）,但是本机调试注意加上以下代码表示模块的查找路径
            `
            cur_dir = os.path.split(os.path.realpath(__file__))[0]
            sys.path.append("%s/" % cur_dir)
            `    
    3.备注
        为防止接口被覆盖
        建议每个模块下Search,Operate下的接口采用统一形式，例如test模块下定义的接口应该为testResult(以防止其他模块有result接口被相互覆盖)
        
	
该项目提供了权限认证与权限管理（基于用户与组）

**请求URL：**
- ` http://127.0.0.1:4901/graphql_api `

**请求方式：**
- POST



**1、生成token：**

- 参数：

```
  {
        "query": "query generate_token($condition: GenerateTokenArgument!){  generate_token(condition:$condition){    access_token    fresh_token  }}",
        "variables": {"condition": {
                 "user_id": "123",  # 同一平台用户唯一标识
				  "app_id": "1",    # 应用平台id
				  "enc_data": "hello"   # 需要加密的json字符串
				  }},
        "operationName": "generate_token"
    }
```

- 返回示例

```
  {"data": {"generate_token": {
        "access_token": "xxx",
        "fresh_token": "xxx"
    }}}
```

**2、刷新token：**

- 参数：

```
  {
        "query": "query fresh_token($condition: FreshTokenArgument!){  fresh_token(condition:$condition){    fresh_token    access_token  }}",
        "variables": {"condition": {
            "fresh_token": "xxx"
        }},
        "operationName": "fresh_token"}
```

- 返回示例

```
  {"data": {"generate_token": {
        "access_token": "xxx",
        "fresh_token": "xxx"
    }}}
```

**3、验证token：**

- 参数：

```
  {
        "query": "query validate_token($condition: ValidateTokenArgument!){  validate_token(condition:$condition){    dec_data    user_id  }}",
        "variables": {"condition": {
            "token": "xx"
			}},
        "operationName": "validate_token"}
```

- 返回示例

```
  {"data": {"generate_token": {
        "dec_data": "xxx",
        "user_id": "xxx"
    }}}
```


**4、注销token：**

- 参数：

```
  {
        "query": "query logout_token($condition: LogoutTokenArgument!){  logout_token(condition:$condition){    action  }}",
        "variables": {"condition": {
            "user_id": "123",
            "app_id": "1"
        }},
        "operationName": "logout_token"}
```

- 返回示例

```
  {"data": {"generate_token": {
        "dec_data": "xxx",
        "user_id": "xxx"
    }}}
```

**5、为用户加权限：**

- 参数：

```
  {
        "query": "query add_permission_for_user($condition: SubObjActArgument!){  add_permission_for_user(condition:$condition){    status  }}",
        "variables": {"condition": {
            "subject": "lijiacai",
            "resource": "/data/",
            "action": "read"
        }},
        "operationName": "add_permission_for_user"}
```

- 返回示例

```
  {"data":{"add_permission_for_user":{
  	"status":false
  }}}
```

**6、为用户加权限：**

- 参数：

```
  {
        "query": "query add_permission_for_user($condition: SubObjActArgument!){  add_permission_for_user(condition:$condition){    status  }}",
        "variables": {"condition": {
            "subject": "lijiacai",
            "resource": "/data/",
            "action": "read"
        }},
        "operationName": "add_permission_for_user"}
```

- 返回示例

```
  {"data":{"add_permission_for_user":{
  	"status":true
  }}}
```

**7、移除权限:用户/组：**

- 参数：

```
  {
        "query": "query remove_permission($condition: SubObjActArgument!){  remove_permission(condition:$condition){    status  }}",
        "variables": {"condition": {
            "subject": "admin3",
            "resource": "/data/",
            "action": "read"
			}},
        "operationName": "remove_permission"}
```

- 返回示例

```
  {"data":{"remove_permission":{
  	"status":true
  }}}
```

**8、判断权限是否存在: 用户/组：**

- 参数：

```
  {
        "query": "query is_permission($condition: SubObjActArgument!){  is_permission(condition:$condition){    status  }}",
        "variables": {"condition": {
            "subject": "admin3",
            "resource": "/data/",
            "action": "read"
			}},
        "operationName": "is_permission"}
```

- 返回示例

```
  {"data":{"is_permission":{
  	"status":true
  }}}
```


**9、删除角色:用户/组：**

- 参数：

```
  {
        "query": "query delete_role($condition: SubArgument!){  delete_role(condition:$condition){    status  }}",
        "variables": {"condition": {
            "subject": "admin3"
			}},
        "operationName": "delete_role"}
```

- 返回示例

```
  {"data":{"delete_role":{
  	"status":true
  }}}
```

**10、为用户查询组：**

- 参数：

```
  {
        "query": "query search_group_for_user($condition: SubArgument!){  search_group_for_user(condition:$condition){    rows{ group }  }}",
        "variables": {"condition": {
            "subject": "admin3"
			}},
        "operationName": "search_group_for_user"}
```

- 返回示例

```
  {"data":{"search_permission_for_user":{
  	"rows":[
		{"group":"xxx"}
	]
  }}}
```

**11、查询某用户所有权限：**

- 参数：

```
  {
        "query": "query search_permission_for_user($condition: SubArgument!){  search_permission_for_user(condition:$condition){    rows{ user resource action}  }}",
        "variables": {"condition": {
            "subject": "admin3"
			}},
        "operationName": "search_permission_for_user"}
```

- 返回示例

```
  {"data":{"search_permission_for_user":{
  	"rows":[
		{"group":"xxx",
		"user":"xxx",
		"resource":"xxx",
		"action":"xxx"
		}
	]
  }}}
```


**12、查询某组所有权限：**

- 参数：

```
  {
        "query": "query search_permission_for_group($condition: GroupArgument!){  search_permission_for_group(condition:$condition){    rows{ group resource action }  }}",
        "variables": {"condition": {
            "group_name": "admin3"
			}},
        "operationName": "search_permission_for_group"}
```

- 返回示例

```
  {"data":{"search_permission_for_group":{
  	"rows":[
		{"group":"xxx",
		"resource":"xxx",
		"action":"xxx"
		}
	]
  }}}
```


**13、为用户添加组,使用户拥有组的权限：**

- 参数：

```
  {
        "query": "query add_group_for_user($condition: SubGroupArgument!){  add_group_for_user(condition:$condition){    status  }}",
        "variables": {"condition": {
            "subject": "user1",
            "group_name": "admin3"
            }},
        "operationName": "add_group_for_user"}
```

- 返回示例

```
  {"data":{"add_group_for_user":{
  	"status":true
  }}}
```

**14、为组移除用户，使用户不再拥有组的权限：**

- 参数：

```
  {
        "query": "query remove_user_for_group($condition: SubGroupArgument!){  remove_user_for_group(condition:$condition){    status  }}",
        "variables": {"condition": {
            "subject": "user1",
            "group_name": "admin3"
            }},
        "operationName": "remove_user_for_group"}
```

- 返回示例

```
  {"data":{"remove_user_for_group":{
  	"status":true
  }}}
```

**15、查询所有组：**

- 参数：

```
  {
        "query": "query search_groups{  search_groups{    rows{ group }  }}",
        "operationName": "search_groups"}
```

- 返回示例

```
  {"data":{"search_permission_for_user":{
  	"rows":[
		{"group":"xxx"}
	]
  }}}
```
            
    
