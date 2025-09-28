

# hytest 自动化测试项目说明

本项目为一个Python语言开发的自动化软件测试项目。 使用了 `hytest` 自动化测试框架。

`hytest`  让大家直接用 Python 来写测试用例，`初始化清除` 机制清晰灵活 ，可以灵活地 **挑选** 要执行的测试用例。



## 安装、执行


安装 hytest 非常简单，执行如下命令即可：

```
pip install hytest 
```

注意： hytest 需要 Python 3.9 或者 更高版本



执行hytest 自动化之前，需要新建一个 `项目目录` ， 里面创建一个名为   `cases`  的子目录用来存放测试用例代码即可。

运行hytest自动化测试，非常简单，只需要

- 打开命令行窗口

- 进入自动化代码根目录，也就是  `cases 的上层目录` 

- 运行 hytest

运行命令  `hytest` 实际上就是执行如下的命令

```
python -m hytest
```



如果你是苹果Mac系统，可以执行命令

```
python3 -m hytest
```

执行后的命令行窗口界面输出，展示了执行每个用例的结果。

执行自动化，会产生一个 `log` 目录。里面有详细的 `测试日志` 和 `测试报告`。

`测试日志` 是 txt文件。

`测试报告` 是HTML格式的，会自动在浏览器中打开，可以通过右上角的浮动菜单：

- 切换 精简、详细 两种模式
  方便浏览内容
  
- 跳转到下一个、上一个错误
  方便在出现问题是，快速定位到问题所在点


测试报告的语言缺省使用操作系统语言，如果要强制指定，只需要加上 参数 `--lang` 

比如

```py
hytest  --lang=en

或者

python -m hytest  --lang=en
```




如果你不希望执行完测试后，自动打开测试报告，可以使用参数  `--auto_open_report=no` 

如下

```py
hytest --auto_open_report=no
```

关于hytest 命令行的参数使用，后面会有详细讲解，以后如果忘了某个命令参数可以执行  `hytest -h`  来查看参数说明。


以后真正做项目自动化的时候，通常还需要创建一些其他的目录，比如

-  `lib`  目录

   用来存放 测试用例 需要使用的共享代码库。


-  `doc`  目录

   存放 一些说明文档



可以使用命令参数  `--new` 来创建一个 hytest 的自动化项目目录，里面会包含一个cases目录和一个示例代码文件。

比如，执行 

```py
hytest --new auto1
```

就会在当前目录下创建名为   `auto1`  的 项目目录。



## 用例目录结构


我们先了解一下用例目录的 结构

  
- `自动化测试用例`  是 写在 python 文件 中的 一个 python 类

   对应一个测试用例文档里面的用例

- 一个 代码文件  可以存放 多个用例
   
- 多个代码文件可以用目录组织起来
  



`cases` 目录下面的 每个目录 和 py 文件 都 被称之为 `测试套件(suite)`  

 `测试套件`  是 `测试用例的集合` ， 通俗的说，就是 `一组用例` 。 

为例方便管理，我们把功能相关的测试用例组合起来放在一起，成为某个测试套件。
   
  
- 包含 测试用例类 的 python 文件 称之为一个  `套件文件` 
   
- 包含 套件文件的 目录 称之为  `测试套件目录` 



## 用例类的定义
 

用例文件格式如下：

文件里面每个类对应一个用例。

- 类的 `name`  属性 指定 用例名
 
  如果没有 name 属性，那么类名就会被当做是用例名称

- 类的  `teststeps`  方法 对应 测试步骤 代码

  测试步骤代码 就是自动化地 一步步执行测试用例 的程序。

  所以一个类 **必须要有 teststeps 方法**，才会被 hytest 当做是一个测试用例类。

比如  

```py
# 建议：类名 对应 用例编号
class UI_0101:
    # 测试用例名字，也建议以用例编号结尾，方便 和 用例文档对应
    # 也方便后面 根据用例名称 挑选执行
    name = '管理员首页 - UI-0101'

    # 测试用例步骤
    def teststeps(self):
```





为了使我们的测试日志和报告 更加清晰的展示执行的过程， 我们可以调用 hytest 的一些库函数，输出 执行步骤、提示信息 、检查点信息。



代码最前面加上 如下代码 ，导入 hytest 库里面 的常用 函数 

```py
from hytest import STEP, INFO, CHECK_POINT

class UI_0101:
      
    def teststeps(self):
        
        STEP(1,'打开浏览器')
        var1 = 'sdf'
        INFO(f'var1 is {var1}')
        CHECK_POINT('打开成功', var1.startswith('1sd') ) 

        
        STEP(2,'登录')        
        CHECK_POINT('检查登录是否成功', True) 
    
        STEP(3,'查看菜单') 
        CHECK_POINT('检查菜单是否正确', True)  
```



- STEP 函数 
   
   用来声明每个测试步骤，这样日志报告更清晰

- INFO 函数 

   用来打印一些信息在日志和报告中，方便出现问题时定位。

   当然，如果你在开发调试阶段也可以直接使用print，在终端查看内容

- CHECK_POINT 函数

   用来声明测试过程中的每个检查点，任何一个检查点不通过，整个测试用例就被认为不通过。
      
   第1个参数是 检查点描述；
   
   第2个参数是 检查点表达式，比如 `result["retcode"] == 0`；
   
   第3个参数是 检查点不通过后是否继续执行该用例后面的代码。 
   
   缺省情况下，一个检查点不通过，该用例teststeps后面的测试代码就不会继续执行。

   如果你希望 某个检查点即使不通过，teststeps 后续代码仍然继续执行，可以使用参数  `failStop=False` ，如下所示

   ```py   
    def teststeps(self):

        CHECK_POINT('即使不通过也不中止1', False, failStop=False)

        CHECK_POINT('即使不通过也不中止2', False, failStop=False)
   ```



## 一个例子

要讲解 自动化测试，需要一个 `被测系统` 。

我们使用  `白月SMS系统`   作为被测系统。

针对该系统，现在有一批测试用例，准备自动化。


我们先完成用例  `UI-0101` 的自动化，用例描述如下


```
- 用例类别
  
  管理员登录

- 前置条件

系统中存在管理员：

账号为 byhy
密码为 88888888	


- 测试步骤

1. 使用正确的管理员账号、密码登录白月SMS系统

2. 检查左侧菜单


- 预期结果

1. 登录成功

2. 前三项菜单名称分别为：
 
客户
药品
订单
```



对应的 hytest 测试用例 参考代码如下


```py
from hytest import *
from selenium import webdriver
from selenium.webdriver.common.by import By

class UI_0101:

    # 用例名
    name =  '检查操作菜单 UI_0101'

    # 测试步骤
    def teststeps(self):

        STEP(1,'登录网站')

        wd = webdriver.Chrome()
        wd.implicitly_wait(10)

        wd.get('http://127.0.0.1/mgr/sign.html')

        wd.find_element(By.ID, 'username').send_keys('byhy')
        wd.find_element(By.ID, 'password').send_keys('88888888')

        wd.find_element(By.TAG_NAME, 'button').click()

        STEP(2,'获取左侧菜单信息')

        eles = wd.find_elements(By.CSS_SELECTOR, '.sidebar-menu li span')

        menuText = [ele.text  for ele in eles]

        INFO(menuText)

        STEP(3,'检查菜单栏')

        CHECK_POINT('左侧菜单检查', menuText[:3] == ['客户','药品', '订单'])

        wd.quit()

```



## 初始化、清除


仔细分析，上面用例要 打开浏览器登陆

如果有100个这样的用例，就执行100次登录的操作。

这些用例 重点其实不在登录，而是后面的操作。

它们后面的操作 需要的初始环境是一样的 ：   `打开浏览器并且登录`  的环境

能不能共享执行环境?

让这些用例开始执行的时候，就处于 打开浏览器并且登录 的环境

就是我们用例执行时，就获取一个 WebDriver对象， 对应  管理员账号已经登录状态 的浏览器，后面的代码直接就可以使用这个 WebDriver对象 执行操作。



怎么 让自动化 用例执行的时候，就有一个 打开浏览器并且登录 的 `初始环境`  呢？

这就需要  `初始化` （英文叫  `setup`  ）操作

初始化 就是： 为 一个或者多个测试用例执行时，构建所需要的数据环境。

与初始化正好相反的操作就是 `清除` （英文叫 `teardown` ）。

初始化 是 创建环境，清除 是  `还原（或者说销毁）` 环境

为什么需要 清除 来 还原环境？

因为 执行完测试用例后 可能会对数据环境产生改变，这种改变后的数据环境，可能会影响 其它用例的执行（不需要这种数据环境的用例）

比如：

用例A 测试系统中存在用户账号，使用该账号进行登录，期望结果是登录成功

用例B 测试系统中没有任何账号，使用不存在的账号进行登录，期望结果是登录失败。

为了执行用例A，我们初始化操作里面创建了一个账号user1

执行完后，需要执行用例B，那么这个创建的user1账号，就破坏了用例B所需要的数据环境（系统中没有账号）

这就需要在执行完用例A 后，执行一个 清除（还原）操作， 把添加的用户账号user1 删除掉。



可能有的朋友说，那也可以在用例B的初始化操作里面删除所有账号啊。

那样做，会使得 每个用例的初始化 工作变得非常难。 因为 不知道自动化测试的时候，会执行哪些用例，这些用例执行后 可能会产生什么多余的数据。

所以一个原则是： 

 `谁` 做的 `初始化` 操作对环境产生了 `什么改变` ， 
 
 `谁` 就应该在 `清除` 操作里面做什么样的 `还原` 。 


hytest 的初始化/清除 支持 `3种方式` 

- 单个用例的初始化、清除
- 整个用例文件的初始化、清除
- 整个用例目录的初始化、清除


### 单个用例

首先看第一种：

单个用例的初始化、清除 是在 用例对应的类里面添加setup、teardown 方法


```py
class c0101:
    name = '管理员首页 - UI-0101'

    # 初始化方法
    def setup(self):
        open_browser()
        mgr_login()

    # 清除方法
    def teardown(self):
        wd = GSTORE['wd']
        wd.quit()

    # 测试用例步骤
    def teststeps(self):        
```



hytest 执行用例时 

- 先执行 setup 里面的代码

- 再执行 teststeps 里面的代码

- 最后再执行 teardown 里面的代码。

而且

如果 setup 执行失败（有异常）， 就不会再执行 teststeps 和 teardown 里面的代码了。

如果 teststeps 执行失败， 仍然会执行 teardown ， 确保环境被 清除



### 用例文件



精明的读者肯定已经发现，上面这种**单个用例**的初始化、清除，并没有解决我们前面说的 **多个用例** 共享数据环境的问题。

这时，我们可以使用  `整个用例文件的初始化、清除` 


就是在 文件中 添加全局函数  `suite_setup`  和  `suite_teardown`  

如下所示

```py
from hytest  import *
from lib.webui import  *
from time import sleep

def suite_setup():
    INFO('suite_setup')
    open_browser()
    mgr_login()

def suite_teardown():
    INFO('suite_teardown')
    wd = GSTORE['wd']
    wd.quit()

class c0101:
    # 测试用例名字
    name = '管理员首页 - UI-0101'

    def teststeps(self):
    # 此处省略 测试用例步骤代码    


class c0102:
    name = '管理员首页 - UI-0102'

    def teststeps(self):
    # 此处省略 测试用例步骤代码    

```



如果一个 用例文件 既有 suite_setup、suite_teardown  ，用例里面也有 setup、teardown , 执行的次序是

- 执行用例文件的 suite_setup， 
  
- 执行文件里面各个 用例 的 setup， teststeps， teardown，

- 最后执行用例文件的 suite_teardown



### 套件目录


刚才我们做到了让一个用例文件里面，所有的用例都共享初始化、清除操作。

如果 多个用例文件里面，的用例都需要相同的初始化清除操作怎么办？
比如目录结构



这时，我们可以使用  `整个用例文件的初始化、清除` 


除了登录测试，其他所有的web界面操作都需要 打开浏览器登录，否则也会导致多次打开浏览器。

可以把打开浏览器的操作设置为 web界面操作目录 共同的初始化

把其他放到 登录后操作 目录中， 添加登录后操作的 初始化

那么怎么设置一个目录共同的初始化呢？

就是 在这个目录下面创建名为  `__st__.py`  的文件。

和套件文件一样，套件目录的 的初始化、清除 也是在 文件中 添加全局函数 suite_setup、suite_teardown。 



如果 套件目录有 suite_setup、suite_teardown，  用例文件也有 suite_setup、suite_teardown  ，用例里面也有 setup、teardown , 执行的次序是

- 执行用例目录的 suite_setup，

- 对该目录下的每个用例文件：
  
    - 执行用例文件的 suite_setup， 
      
    - 执行文件里面各个 用例 的 setup， teststeps， teardown，

    - 执行用例文件的 suite_teardown

- 执行用例目录的 suite_teardown




### 缺省初始化、清除

`用例文件`   除了 可以使用 suite_setup、suite_teardown 对整个套件进行初始化清除，还支持另外一种初始化清除： `缺省初始化、清除` 

就是定义 名称为  `test_setup`  和  `test_teardown` 的全局函数。

如果在 用例文件 中定义了 全局函数 `test_setup` ， 该文件中某个用例  `本身没有初始化` 方法， 执行自动化的时候就会 使用这个 `test_setup` 来初始化

如果在 用例文件 中定义了 全局函数 `test_teardown` ，该文件中某个用例  `本身没有清除` 方法， 执行自动化的时候就会 使用这个 `test_teardown` 来清除





## 数据关联

### 用法

在初始化操作里面，经常会有创建一些数据，这些数据要在后面的用例中使用。

这对于 用例类内部的初始化数据方法setup 来说，很简单， 因为测试步骤和清除方法的都是同一个类的。

hytest框架执行时，会为该类创建实例。 所以只需要放入实例属性即可



对于 用例文件或者 整个套件目录的初始化函数， 怎么把  `suite_setup` 函数  产生的数据给里面的用例使用呢？ 

前面示例其实已经讲过，可以使用hytest内置的对象  `GSTORE`

这个 GSTORE 

可以使用字典式的赋值和取出元素，比如 

```py
from hytest import GSTORE

def suite_setup():
    GSTORE['环境1产品id'] = createProduct()
    GSTORE['driver'] = webdriver.Chrome()

def suite_teardown():
    deleteProduct(GSTORE['环境1产品id'])
    GSTORE['driver'].quit()


class c00303:
    name = '添加订单 - API-0303'

    def teststeps(self):
        createOrder(productid=GSTORE['环境1产品id'])
```



GSTORE 也可以进行属性赋值和取值，比如


```py
def suite_setup():
    GSTORE.productId = createProduct()
    GSTORE.driver = webdriver.Chrome()

def suite_teardown():
    deleteProduct(GSTORE.productId)
    GSTORE.driver.quit()


class c00303:
    name = '添加订单 - API-0303'

    def teststeps(self):
        createOrder(productid=GSTORE.productId)
```

这样写起来更简单，但是属性名要符合python的变量名规则，就不能有空格、加减号 之类的字符了。


### 依赖注入

如果觉得代码中使用  `GSTORE.data1` 或者  `GSTORE['data1']` 这样的写法太麻烦，可以使用 **依赖注入** 来解决

直接把你需要的 GSTORE里面的对象名称作为参数，传递给 `teststeps`方法，或者 初始化清除方法/函数 。

hytest 框架在调用这些方法的时候，会检查参数，自动把 GSTORE里面的同名对象赋值给该参数。

比如

```py
def suite_setup():
    GSTORE.productId = createProduct()
    GSTORE.driver = webdriver.Chrome()

def suite_teardown(driver):
    deleteProduct(GSTORE.productId)
    driver.quit()


class c00303:
    name = '添加订单 - API-0303'

    def teststeps(self, productId):
        createOrder(productid=productId)    
```

### IDE 类型提示

使用内置的GSOTRE有个缺点，就是不知道添加的数据类型，IDE没法辅助，比如不能自动补齐对象的方法。

其实可以自己定义全局存储对象，并且定义里面的数据和类型。

比如，可以在项目根目录下面创建一个share.py文件，内容如下


```py
from selenium import webdriver
class gs:
    driver : webdriver.Chrome 
    productId : int
```

然后用例文件、 `__st__.py`  文件就可以这样使用了

```py
from share import gs

def suite_setup():
    gs.productId = createProduct()
    gs.driver = webdriver.Chrome()

def suite_teardown():
    deleteProduct(gs.productId)
    gs.driver.quit()


class c00303:
    name = '添加订单 - API-0303'

    def teststeps(self):
        createOrder(productid=gs.productId)
```



gs 定义的时候，里面的各个属性就有类型声明，后面使用该属性时，IDE就可以进行代码辅助了。



## 数据驱动 - data driven


做过自动化测试的朋友经常听说过 `数据驱动` （或者面试的时候被问到过）。

什么是数据驱动？


如果有一批测试用例，具有 `相同的测试步骤` ，只是 `测试参数数据不同` 。 

自动化测试时，把测试数据从用例代码中 `分离` 开来，以后增加新的测试用例，只需要修改数据。

这就是数据驱动。



举个例子：

某系统 登录功能的测试，有一批测试用例，其执行的步骤几乎都是一样的，只是使用的测试参数不同。

比如：

- 不输入用户名，输入正确密码

- 输入比正确用户名后面少一个字符，输入正确密码

- 输入比正确用户名后面多一个字符，输入正确密码

- 输入比正确用户名前面少一个字符，输入正确密码

- 输入比正确用户名前面多一个字符，输入正确密码

- 输入正确用户名，不输入密码

- 输入正确用户名，输入比正确密码后面多一个字符




这种情况可以使用 hytest用例 的 数据驱动格式，只需如下定义即可

```py
class c00003x:
    # ddt_cases 里面每个字典元素 定义一个用例的数据
    # 其中： name是该用例的名称， para是用例的参数
    ddt_cases = [
        {
            'name' : '登录 - 000031',
            'para' : ['user001','888888']
        },
        {
            'name' : '登录 - 000032',
            'para' : ['user0012','888888']
        },
        {
            'name' : '登录 - 000033',
            'para' : ['ser001','888888']
        }
    ]
    
    # 调用时，
    # hytest 框架执行时，会自动创建出3个用例实例
    # 并且在调用 teststeps时，把每个用例的参数设置在 self.para 中
    # 用例代码 可以直接从 self.para 中获取参数  
    def teststeps(self):
        # 取出参数
        username, password = self.para
        
        # 下面是登录测试代码
```

这样，我们就不需要定义那么多的测试用例类了， 而且测试数据也可以集中存放。

特别要注意的是： 一旦使用数据驱动定义了用例，那么这些用例的名字就不是类名（比如上面代码里面的 `UI_000x`），而是驱动里面定义的名称了（比如 `登录 UI_0001` ， `登录 UI_0002` ， `登录 UI_0003` ）。

所以，在执行测试的时候， 通过命令行参数 挑选上面的所有用例， 就应该是 `hytest --test 登录*`, 而不是 `hytest --test UI_000x` 



### 动态产生驱动数据


hytest 的驱动数据通常是固定的数据，当然也可以产生一些动态的数据

比如

```py
from hytest import *

class UI_000x:

    ddt_cases = []
    for i in range(10):
        ddt_cases.append({
            'name': f'登录 UI_000{i+1}',
            'para': [None, f'{i+1}'*8,'请输入用户名']
        })
 
    def teststeps(self):
        INFO(f'{self.para}')
```



hytest 的运行分为两个阶段

- 收集测试用例

  这个阶段会搜集所有的用例目录下面的代码中的用例类，
  
  把这些类实例化， 从而创建  `用例实例对象` 

- 执行测试用例

  依次执行 上一步中创建的 `用例实例对象`



所以第一步中  **搜集创建用例对象，是在 执行用例之前** 的

所以ddt_cases 里面  **不能使用用例运行时 才会产生的数据** 。

比如

```py
from hytest import *
 
# 套件初始化
def suite_setup():
    GSTORE['ddt_cases_UI_000x'] = []    
    for i in range(10):
        GSTORE['ddt_cases_UI_000x'].append({
            'name': f'登录 UI_000{i+1}',
            'para': [None, f'{i+1}'*8,'请输入用户名']
        }) 
  
class UI_000x:
    # 想使用套件初始化 设置的GSTORE数据？？不行！！！！ 
    # 因为 ddt_cases 收集阶段就会执行，这时还没有执行suite_setup()
    # 这时 GSTORE里面还是空的，所以会报错
    ddt_cases = GSTORE['ddt_cases_UI_000x']

    def teststeps(self):
        INFO(f'{self.para}')
```


## 挑选用例执行 - 名称方式


执行自动化测试的时候，我们往往并不需要执行 `全部的` 测试用例。

比如：冒烟测试，只需要测试冒烟测试的那些用例。 或者调试自己写的某个用例的自动化，就只需要执行那一个用例。

hytest  可以灵活的挑选要执行的测试用例。



我们可以通过  `--test`  或者  `--suite`  命令行参数 来指定执行哪些用例或者套件，而且还支持用通配符的方式。

```py
--test testA                # 执行名为 testA 的用例
--test testA --test testB  # 执行名为 testA 和  testB 的用例
--test test*              # 执行名字以 test 开头的用例
--suite 订单管理              # 执行 名为 订单管理 的套件
```


比如，我们想只测试  `药品管理`   这个套件

```
hytest --suite  药品管理  
```


比如，我们想只测试  `界面 - UI-0101`   这个用例

```
hytest --test  "界面 - UI-0101"  
```

因为用例名中有空格，所以必须用双引号包起来。

通常，我们的用例名后面会包含用例的 ID，  这样就可以很方便的根据用例ID，来选择用例了

比如 这样

```
hytest --test  *0101  
```

就可以挑选我们 练习中的 用例名为  `界面 - UI-0101` 的用例执行




假如，你的测试领导，要求做冒烟测试， 挑选出来的用例编号为以下这些：

```
UI-0301
UI-0302
UI-0303
UI-1401
UI-1402
```

我们就可以这样执行 

```
hytest --test *0301  --test *0302 --test *0303 --test *1401 --test *1402
```

大家自然会想到，如果要执行的用例太多，比如 1000 个，命令行参数岂非太长了？


这时我们可以使用参数文件，可以把所有的参数都放在参数文件中，比如，创建一个名字为 args 的参数文件，内容如下

```
--test *0301
--test *0302
--test *0303
--test *1401
--test *1402
```

一行一个参数

然后， 我们的命令就只需要   `hytest -A args`  就可以了



## 挑选用例执行 - 标签方式

hytest  还有一种选择测试用例的方法：根据用例的 `标签` 来挑选用例

### 给用例添加标签


我们可以给测试用例打上标签（tag），这样在运行的时候，可以通过标签指定要运行哪些用例。

标签 就是用例的属性特征描述

测试用例可以有多个标签描述它的属性特征， 比如一个登录测试的用例， 可以有3个标签： 登录功能、冒烟测试、UI测试

hytest 可以根据设置的标签 选择执行该用例。 这个后面会讲



给用例添加标签有如下几种方式

- 全局变量 force_tags

如果我们在测试用例文件 定义了一个名为 force_tags 的全局变量，格式如下

```py
force_tags = ['登录功能','冒烟测试','UI测试']
```

那么该文件里面所有测试用例都具有了这些标签。

标签一定要放在列表中，即使只有一个标签



如果我们在测试套件目录初始化文件__st__.py定义了一个这样的 force_tags 全局变量, 那么该目录里面所有测试用例都具有了该tag


- 测试用例类的 tags 属性
  
如果我们在测试用例类 定义了一个名为 tags 属性，格式如下

```py
class c00001:
    name = '添加订单 - 00001'
    # 用例标签，可选   
    tags = ['登录功能','冒烟测试','UI测试']
```

那么本测试用例就具有了这些标签。


### 根据标签挑选


在执行自动化的时候，我们可以通过命令行参数，指定标签，从而挑选要执行的测试用例

比如：

```py
# 执行包含 标签 '冒烟测试' 的用例. 
--tag 冒烟测试  


# 执行不包含标签 '冒烟测试' 的用例.
--tagnot 冒烟测试 


# 执行 同时有 冒烟测试、UITest 两个标签的用例
--tag "'冒烟测试' and 'UITest'"


# 执行 有 冒烟测试 或者 UITest 标签 的用例
--tag 冒烟测试   --tag UITest


# 执行标签格式为 A*B 的用例，比如 A5B， AB， A444B
--tag A*B    
```

