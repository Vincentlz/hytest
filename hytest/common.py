from .utils.signal import signal
from .utils.runner import Runner, CheckPointFail
from .cfg import l

from datetime import datetime
import inspect
import ast
import executing 

class _GlobalStore:
    def __getitem__(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            return default
        
    def __setitem__(self,key,value):
        setattr(self, key, value )

    get = __getitem__

# used for storing global shared data
GSTORE = _GlobalStore()

def INFO(info):
    """
    print information in log and report.
    This will not show in terminal window.

    Parameters
    ----------
    info : object to print
    """
    signal.info(f'{info}')

def STEP(stepNo:int,desc:str):
    """
    print information about test steps in log and report .
    This will not show in terminal window.


    Parameters
    ----------
    stepNo : step number
    desc :   description about this step
    """
    signal.step(stepNo,desc)



OP_MAP = {
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.Is: "is",
    ast.IsNot: "is not",
    ast.In: "in",
    ast.NotIn: "not in",
}

def CHECK_POINT(desc:str, condition, failStop=True, failLogScreenWebDriver = None):
    """
    check point of testing.
    pass or fail of this check point depends on argument condition is true or false.
    it will print information about check point in log and report.

    Parameters
    ----------
    desc :    check point description, like check what.
    condition : usually it's a bool expression, like  `a==b`, 
        so actually, after evaluating the expression, it's a result bool object passed in .
    failStop : switch for whether continue executing test case when the condition value is false 
    failLogScreenWebDriver : Selenium web driver object,
        when you want a screenshot image of browser in test report if current check point fail.
    """

    # ✅  check point pass
    if condition:
        signal.checkpoint_pass(desc)
        return
    
    # ❌  check point fail
    try:
        caller_frame = inspect.currentframe().f_back

        # 获取调用节点    
        ex = executing.Source.executing(caller_frame)
        call_node = ex.node

        compaireInfo = ''
        
        # 确保拿到了一个调用节点
        if isinstance(call_node, ast.Call):

            arg_node = call_node.args[1]

            # 如果是比较运算符
            if isinstance(arg_node, ast.Compare):                

                # * 反解析参数节点以获得完整表达式 ➡️🔍💲⬅️❌ 🔔💡 *
                full_expression_str = ast.unparse(arg_node).strip()
                compaireInfo += (f"\n\n 🔎 {full_expression_str} ")

                left_expr_str = ast.unparse(arg_node.left).strip()
                right_expr_str = ast.unparse(arg_node.comparators[0]).strip()

                # op_node = arg_node.ops[0]
                # op_str = OP_MAP.get(type(op_node), "未知比较操作符")

                caller_globals = caller_frame.f_globals
                caller_locals = caller_frame.f_locals

                left_val = eval(left_expr_str, caller_globals, caller_locals)
                right_val = eval(right_expr_str, caller_globals, caller_locals)

                left_expr_value = repr(left_val)
                right_expr_value = repr(right_val)
                
                left_expr_value = left_expr_value if len(left_expr_value) < 2000 else f"{left_expr_value} ..."
                right_expr_value = right_expr_value if len(right_expr_value) < 2000 else f"{right_expr_value} ..."

                compaireInfo += (f"\n 💲 {('左边','left  ')[l.n]} 🟰 {left_expr_value}")
                # print(f"💡 {op_str}")
                compaireInfo += (f"\n 💲 {('右边','right ')[l.n]} 🟰 {right_expr_value}")

        else:
            print(("⚠️  无法获取 CHECK_POINT condition 参数", "⚠️  Could not identify the condition parameter of CHECK_POINT. ")[l.n])

    except Exception as e:
        print(f"  (Could not introspect expression: {e})")
    finally:
        if 'caller_frame' in locals():
            del caller_frame


    signal.checkpoint_fail(desc + compaireInfo)

    # 如果需要截屏
    if failLogScreenWebDriver is not None:
        SELENIUM_LOG_SCREEN(failLogScreenWebDriver)

    # 记录下当前执行结果为失败
    Runner.curRunningCase.execRet='fail'
    Runner.curRunningCase.error=('检查点不通过','checkpoint failed')[l.n]
    Runner.curRunningCase.stacktrace="\n"*3+('具体错误看测试步骤检查点','see checkpoint of case for details')[l.n]
    # 如果失败停止，中止此测试用例
    if failStop:
        raise CheckPointFail()

def LOG_IMG(imgPath: str, width: str = None):
    """
    add image in test report

    Parameters
    ----------
    imgPath: the path of image
    width:  display width of image in html, like 50% / 800px / 30em 
    """

    signal.log_img(imgPath, width)


def SELENIUM_LOG_SCREEN(driver, width: str = None):
    """
    add screenshot image of browser into test report when using Selenium
    在日志中加入selenium控制的 浏览器截屏图片

    Parameters
    ----------
    driver: selenium webdriver
    width:  display width of image in html, like 50% / 800px / 30em 
    """
    filename = datetime.now().strftime('%Y%m%d%H%M%S%f')
    filepath = f'log/imgs/{filename}.png'
    filepath_relative_to_log = f'imgs/{filename}.png'
    driver.get_screenshot_as_file(filepath)
    signal.log_img(filepath_relative_to_log, width)