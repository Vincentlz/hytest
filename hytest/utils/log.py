import logging, os, time, traceback, platform
import shutil
from logging.handlers import RotatingFileHandler


from rich.console import Console
from rich.theme import Theme

from hytest.product import version

from datetime import datetime

from hytest.common import GSTORE

from .runner import Collector
from ..cfg import l,Settings

os.makedirs('log',exist_ok=True)

# 日志文件
logger = logging.getLogger('my_logger') 
logger.setLevel(logging.DEBUG)

logFile = os.path.join('log','testresult.log')
handler = RotatingFileHandler(
    logFile, 
    maxBytes=1024*1024*30, 
    backupCount=2,
    encoding='utf8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(message)s')
handler.setFormatter(formatter)

handler.doRollover() # 每次启动创建一个新log文件，而不是从原来的基础上继续添加

logger.addHandler(handler)


# # 重定向stdout，改变print行为，同时写屏和日志
# import sys
# class MyPrintClass:
 
#     def __init__(self):
#         self.console = sys.stdout

#     def write(self, message):
#         self.console.write(message)
#         logger.info(message)
 
#     def flush(self):
#         self.console.flush()
#         # self.file.flush()

# sys.stdout = MyPrintClass()



console = Console(theme=Theme(inherit=False))

print = console.print



class LogLevel:
    """
    here, we use different log level numbers with Python logging lib
    CRITICAL - 0
    ERROR    - 1
    WARNING  - 2
    INFO     - 3
    DEBUG    - 4
    ALL      - 5
    """
    level = 3



class Stats:

    def test_start(self,_title='Test Report'):
        self.result = {
            # 这是准备执行的用例数量
            'case_count_to_run': Collector.case_number,
            # 这个是实际执行的用例数量，可能有其他的用例因为初始化失败没有执行
            'case_count' : 0,
            'case_pass'  : 0,
            'case_fail'  : 0,
            'case_abort' : 0,
            'suite_setup_fail' : 0,
            'case_setup_fail' : 0,
            'suite_teardown_fail' : 0,
            'case_teardown_fail' : 0,
            'case_pass_list'  : [],
            'case_fail_list'  : [],
            'case_abort_list' : [],

        }
                
    
        self.start_time = time.time()

    def test_end(self, runner):
        self.end_time = time.time()
        self.test_duration = self.end_time-self.start_time

        if  self.result['case_fail'] or \
            self.result['case_abort'] or \
            self.result['suite_setup_fail'] or \
            self.result['case_setup_fail'] or \
            self.result['suite_teardown_fail'] or \
            self.result['case_teardown_fail'] :
            GSTORE['---ret---'] = 1
        else:
            GSTORE['---ret---'] = 0


    def enter_case(self, caseId ,name, case_className):
        self.result['case_count'] += 1    
    

    def case_result(self,case):
        if case.execRet == 'pass':
            self.result['case_pass'] += 1   
        elif case.execRet == 'fail':
            self.result['case_fail'] += 1  
        elif case.execRet == 'abort':
            self.result['case_abort'] += 1   


    # utype 可能是 suite  case  case_default     
    def setup_fail(self,name, utype, e, stacktrace):  
        if utype.startswith('suite'):
            self.result['suite_setup_fail'] += 1   
        else:
            self.result['case_setup_fail'] += 1 
    
    def teardown_fail(self,name, utype, e, stacktrace):  
        if utype.startswith('suite'):
            self.result['suite_teardown_fail'] += 1   
        else:
            self.result['case_teardown_fail'] += 1 

stats = Stats()

class ConsoleLogger:
    
    def test_end(self, runner):
        ret = stats.result
        print((f'\n\n  ========= 测试耗时 : {stats.test_duration:.3f} 秒 =========\n',
               f'\n\n  ========= Duration Of Testing : {stats.test_duration:.3f} seconds =========\n')[l.n])


        print(f"\n  {('预备执行用例数量','number of cases plan to run')[l.n]} : {ret['case_count_to_run']}")

        print(f"\n  {('实际执行用例数量','number of cases actually run')[l.n]} : {ret['case_count']}")

        print(f"\n  {('通过','passed')[l.n]} : {ret['case_pass']}", style='green')
        
        num = ret['case_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  {('失败','failed')[l.n]} : {num}", style=style)
        
        num = ret['case_abort']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  {('异常','exception aborted')[l.n]} : {num}", style=style)
        
        num = ret['suite_setup_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  {('套件初始化失败','suite setup failed')[l.n]} : {num}", style=style)
        
        num = ret['suite_teardown_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  {('套件清除  失败','suite teardown failed')[l.n]} : {num}", style=style)
        
        num = ret['case_setup_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  {('用例初始化失败','cases setup failed')[l.n]} : {num}", style=style)
        
        num = ret['case_teardown_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  {('用例清除  失败','cases teardown failed')[l.n]} : {num}", style=style)

        print("\n\n")
    
    def enter_suite(self,name,suitetype):   
        if suitetype == 'file' :
            print(f'\n\n>>> {name}',style='bold bright_white')

    
    def enter_case(self, caseId ,name, case_className):        
        print(f'\n* {name}',style='bright_white')

    
    def case_steps(self,name):...

    
    # def case_pass(self, case, caseId, name):
    #     print('                          PASS',style='green')

    
    # def case_fail(self, case, caseId, name, e, stacktrace):
    #     print(f'                          FAIL\n{e}',style='bright_red')
        
    
    # def case_abort(self, case, caseId, name, e, stacktrace):
    #     print(f'                          ABORT\n{e}',style='magenta')


    def case_result(self,case):
        if case.execRet == 'pass':
            print('                          PASS',style='green')
        elif case.execRet == 'fail':
            print(f'                          FAIL\n{case.error}',style='bright_red')
        elif case.execRet == 'abort':
            print(f'                          ABORT\n{case.error}',style='magenta')


    
    def setup_begin(self,name, utype):...
    
    
    def teardown_begin(self,name, utype):...

    # utype 可能是 suite  case  case_default
    def setup_fail(self,name, utype, e, stacktrace): 
        utype =  ('套件','suite')[l.n] if utype.startswith('suite') else ('用例','case')[l.n]
        print(f"\n{utype} {('初始化失败','setup failed')[l.n]} | {name} | {e}",style='bright_red')
        # print(f'\n{utype} setup fail | {name} | {e}',style='bright_red')

    
    def teardown_fail(self,name, utype, e, stacktrace):      
        utype =  ('套件','suite')[l.n] if utype.startswith('suite') else ('用例','case')[l.n]
        print(f"\n{utype} {('清除失败','teardown failed')[l.n]} | {name} | {e}", style='bright_red')
        # print(f'\n{utype} teardown fail | {name} | {e}',style='bright_red')


    def info(self, msg):
        if LogLevel.level >= 3:
            print(f'{msg}')

    def debug(self, msg):
        if LogLevel.level >= 4:
            print(f'{msg}')

    def error(self,msg):
        if LogLevel.level >= 1:
            print(f'{msg}', style='bright_red')


    def critical(self,msg):
        if LogLevel.level >= 0:
            print(f'{msg}', style='green')



class TextLogger:

    def test_start(self,_title=''):
        startTime = time.strftime('%Y%m%d_%H%M%S',
                                           time.localtime(stats.start_time))

        logger.info(f'\n\n  ========= {("测试开始","Test Start")[l.n]} : {startTime} =========\n')


    def test_end(self, runner):
        endTime = time.strftime('%Y%m%d_%H%M%S',
                                  time.localtime(stats.end_time))
        logger.info(f'\n\n  ========= {("测试结束","Test End")[l.n]} : {endTime} =========\n')

        logger.info(f"\n  {('耗时','Duration Of Testing ')[l.n]}    : {(stats.end_time-stats.start_time):.3f} 秒\n")
        ret = stats.result

        logger.info(f"\n  {('预备执行用例数量','number of cases plan to run')[l.n]} : {ret['case_count_to_run']}")
        logger.info(f"\n  {('实际执行用例数量','number of cases actually run')[l.n]} : {ret['case_count']}")
        logger.info(f"\n  {('通过','passed')[l.n]} : {ret['case_pass']}")
        logger.info(f"\n  {('失败','failed')[l.n]} : {ret['case_fail']}")
        logger.info(f"\n  {('异常','exception aborted')[l.n]} : {ret['case_abort']}")
        logger.info(f"\n  {('套件初始化失败','suite setup failed')[l.n]} : {ret['suite_setup_fail']}")
        logger.info(f"\n  {('套件清除  失败','suite teardown failed')[l.n]} : {ret['suite_teardown_fail']}")
        logger.info(f"\n  {('用例初始化失败','cases setup failed')[l.n]} : {ret['case_setup_fail']}")
        logger.info(f"\n  {('用例清除  失败','cases teardown failed')[l.n]} : {ret['case_teardown_fail']}")
    
    def enter_suite(self,name,suitetype): 
        logger.info(f'\n\n>>> {name}')

    
    def enter_case(self, caseId ,name , case_className):
        curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'\n* {name}  -  {curTime}')

    
    def case_steps(self,name):  
        logger.info(f'\n  [ case execution steps ]')

    
    # def case_pass(self, case, caseId, name):
    #     logger.info('  PASS ')

    
    # def case_fail(self, case, caseId, name, e, stacktrace):
    #     logger.info(f'  FAIL   {e} \n{stacktrace}')
        
    
    # def case_abort(self, case, caseId, name, e, stacktrace):
    #     logger.info(f'  ABORT   {e} \n{stacktrace}')


    def case_result(self,case):
        if case.execRet == 'pass':
            logger.info('  PASS ')
        else:
            if case.execRet == 'fail':                    
                logger.info(f'  FAIL\n\n{case.stacktrace}')


            elif case.execRet == 'abort':
                logger.info(f'  ABORT\n\n{case.stacktrace}')



    
    def setup_begin(self,name, utype): 
        logger.info(f'\n[ {utype} setup ] {name}')
    
    
    def teardown_begin(self,name, utype): 
        logger.info(f'\n[ {utype} teardown ] {name}')

    
    def setup_fail(self,name, utype, e, stacktrace):  
        logger.info(f'{utype} setup fail | {e} \n{stacktrace}')

    
    def teardown_fail(self,name, utype, e, stacktrace):  
        logger.info(f'{utype} teardown fail | {e} \n{stacktrace}')

    
    def info(self, msg):
        if LogLevel.level >= 3:
            logger.info(f'{msg}')

    def debug(self, msg): 
        if LogLevel.level >= 4:
            logger.info(f'{msg}')

    def error(self,msg):
        if LogLevel.level >= 1:
            logger.info(f'{msg}')


    def critical(self,msg):
        if LogLevel.level >= 0:
            logger.info(f'{msg}')

    def step(self,stepNo,desc):
        logger.info((f'\n-- 第 {stepNo} 步 -- {desc} \n',
                     f'\n-- Step #{stepNo} -- {desc} \n',
                     )[l.n])

    def checkpoint_pass(self, desc):
        logger.info((f'\n** 检查点 **  {desc} ---->  通过\n',
                     f'\n** checkpoint **  {desc} ---->  pass\n'
                     )[l.n])
        
    def checkpoint_fail(self, desc, compaireInfo):
        logger.info((f'\n** 检查点 **  {desc} ---->  !! 不通过!!\n',
                     f'\n** checkpoint **  {desc} ---->  !! fail!!\n'
                     )[l.n])
        logger.info(compaireInfo)


    def log_img(self,imgPath: str, width: str = None):
        logger.info(f'picture {imgPath}')


from dominate.tags import *
from dominate.util import raw
from dominate import document

class HtmlLogger:

    def __init__(self):
        self.curEle = None
        # 保存一个  用例文件名 -> htmlDiv对象 的表，因为执行到用例文件清除的时候，要在 用例文件Div对象里面添加 该文件teardown的子节点Div
        self.suiteFileName2DivTable = {}

    def _meta_item(self, label_text, value_text):
        return div(
            span(label_text, _class='meta_label'),
            span(value_text, _class='meta_value'),
            _class='meta_item')

    def _summary_card(self, caption, value, hint, tone):
        return div(
            span(caption, _class='summary_caption'),
            span(str(value), _class='summary_value'),
            span(hint, _class='summary_hint'),
            _class=f'summary_card is-{tone}')

    def _table_row(self, label_text, value, tone=None):
        value_ele = str(value) if tone is None else span(str(value), _class=f'cell_value is-{tone}')
        return tr(th(label_text), td(value_ele))
        
    def test_start(self,_title=''):
        libDir = os.path.dirname(__file__)
        # css file
        with open(os.path.join(libDir , 'report.css'), encoding='utf8') as f:
            _css_style = f.read()
        # js file
        with open(os.path.join(libDir , 'report.js'), encoding='utf8') as f:
            _js = f.read()

        # icon file
        

        self.doc = document(title= Settings.report_title)
        self.doc.head.add(
                        meta(charset="UTF-8"),
                        meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                        link(rel='icon', type="image/png" , href=os.path.join(libDir, 'icon.png')),
                        style(raw(_css_style)),
                        script(raw(_js), type='text/javascript'))

        self.main = self.doc.body.add(div(_class='main_section'))

        self.statusBadgeEle = span(_class='status_badge status-running')
        self.headerMetaEle = div(_class='header_meta')
        self.summaryCardsEle = div(_class='summary_cards')

        reportSubtitle = (
            '聚焦执行结果、失败定位与关键统计，适合日常回归和持续集成场景。',
            'A cleaner execution view for regression runs, failure triage, and daily CI visibility.'
        )[l.n]

        self.main.add(
            div(
                div('HYTEST REPORT', _class='report_kicker'),
                div(
                    div(
                        h1(f'{Settings.report_title}'),
                        p(reportSubtitle, _class='report_subtitle'),
                        _class='report_title_block'
                    ),
                    self.statusBadgeEle,
                    _class='report_header_main'
                ),
                self.headerMetaEle,
                _class='report_header'
            )
        )

        summarySection = self.main.add(div(_class='summary_section'))
        summarySection.add(
            div(
                div(
                    h2(('统计结果','Test Statistics')[l.n]),
                    p(
                        ('从用例规模、通过率和异常分布快速把握本次执行质量。',
                         'Quickly understand scope, pass rate, and issue distribution for this run.')[l.n]
                    )
                ),
                _class='section_intro'
            )
        )
        summarySection.add(self.summaryCardsEle)

        resultDiv = summarySection.add(div(_class='result'))

        self.result_table = table(_class='result_table')
        resultDiv.add(
            div(
                div(
                    div(
                        div(('统计明细','Execution Details')[l.n], _class='panel_title'),
                        p(
                            ('包含时间、执行规模和失败细项。',
                             'Timing, execution scale, and detailed issue counts.')[l.n],
                            _class='panel_desc'
                        )
                    ),
                    _class='panel_header'
                ),
                self.result_table,
                _class='panel'
            )
        )

        self.result_barchart = div(_class='result_barchart')
        resultDiv.add(
            div(
                div(
                    div(
                        div(('分布概览','Distribution Overview')[l.n], _class='panel_title'),
                        p(
                            ('用条形占比快速识别通过、失败、异常与阻塞情况。',
                             'Compare pass, fail, abort, and blocked cases at a glance.')[l.n],
                            _class='panel_desc'
                        )
                    ),
                    _class='panel_header'
                ),
                self.result_barchart,
                _class='panel'
            )
        )

        logSection = self.main.add(div(_class='log_section'))
        logSection.add(
            div(
                div(
                    h2(('执行日志','Test Execution Log')[l.n]),
                    p(
                        ('按目录、文件与用例分层展开，便于定位失败现场。',
                         'Grouped by folder, file, and case to help pinpoint failures quickly.')[l.n]
                    )
                ),
                _class='log_header'
            )
        )
        self.logDiv = logSection.add(div(_class='exec_log'))

        # 查看上一个和下一个错误的 
        self.errorCounterEle = div(
            ('无异常','No Errors')[l.n],
            _class='menu-item menu-item-static',
            id='error_counter',
            **{
                'data-empty-label': ('无异常','No Errors')[l.n],
                'data-prefix-label': ('异常','Errors')[l.n],
            }
        )
        self.ev = div(
                self.errorCounterEle,
                div('∧', _class = 'menu-item error-nav', onclick="previous_error()", title=('上一个异常','Previous Error')[l.n]), 
                div('∨', _class = 'menu-item error-nav', onclick="next_error()", title=('下一个异常','Next Error')[l.n]),
                _class = 'error_jumper',
                style='display:none;'
            )

        helpLink = ("http://www.byhy.net/tut/auto/hytest/01",'https://github.com/jcyrss/hytest/Documentation.md') [l.n]

        displayModeEle = div(
            ('详细模式','Detail Mode')[l.n],
            _class='menu-item',
            id='display_mode',
            onclick="toggle_folder_all_cases()",
            **{
                'data-summary-label': ('概要模式','Summary Mode')[l.n],
                'data-detail-label': ('详细模式','Detail Mode')[l.n],
                'data-summary-title': ('点击切换到详细模式','Switch to detail mode')[l.n],
                'data-detail-title': ('点击切换到概要模式','Switch to summary mode')[l.n],
            }
        )
         
        self.doc.body.add(div(
            div(('页首','Home')[l.n], _class = 'menu-item',
                onclick='document.querySelector("body").scrollIntoView()'),
            div(('帮助','Help')[l.n], _class = 'menu-item', 
                onclick=f'window.open("{helpLink}", "_blank"); '),
            displayModeEle,
            self.ev,
            id='float_menu')
        )

        self.curEle = self.main  # 记录当前所在的 html element
        self.curSuiteEle = None   # 记录当前的套件元素
        self.curCaseEle = None   # 记录当前的用例元素
        self.curCaseLableEle = None   # 记录当前的用例里面的 种类标题元素
        self.curSetupEle = None   # 记录当前的初始化元素
        self.curTeardownEle = None   # 记录当前的清除元素
        self.suitepath2element = {}


    
    def test_end(self, runner):

        execStartTime = time.strftime('%Y/%m/%d %H:%M:%S',
                                           time.localtime(stats.start_time))
        execEndTime = time.strftime('%Y/%m/%d %H:%M:%S',
                                           time.localtime(stats.end_time))

        ret = stats.result

        errorNum = 0
        case_count_to_run = ret['case_count_to_run']
        blocked_num = max(case_count_to_run - ret['case_pass'] - ret['case_fail'] - ret['case_abort'], 0)

        def percentCalc(upper, lower):
            if lower == 0:
                return '0'

            percent = str(round(upper * 100 / lower, 1))
            percent = percent[:-2] if percent.endswith('.0') else percent
            return percent

        def add_barchar_item(statName, amount, percent, color):
            if isinstance(percent, str):
                percent_value = float(percent)
            else:
                percent_value = percent

            barPercent = 1 if 0 < percent_value <= 1 else percent_value
            barPercent = max(barPercent, 0)
            percentStr = f'{percent_value}%'

            self.result_barchart.add(
                div(
                    div(
                        span(f'{statName} · {amount} {("个","")[l.n]}', _class='metric_name'),
                        span(percentStr, _class='metric_percent'),
                        _class='metric_row'
                    ),
                    div(
                        div(
                            "",
                            style=f'width: {barPercent}%; background-color: {color};',
                            _class="barchart_bar",
                        ),
                        _class="barchart_barbox"
                    ),
                    _class="barchar_item"
                )
            )

        execution_rate = percentCalc(ret['case_count'], case_count_to_run)
        pass_rate = percentCalc(ret['case_pass'], case_count_to_run)
        fail_rate = percentCalc(ret['case_fail'], case_count_to_run)
        abort_rate = percentCalc(ret['case_abort'], case_count_to_run)
        blocked_rate = percentCalc(blocked_num, case_count_to_run)

        trs = []        
        trs.append(self._table_row(('hytest 版本','hytest version')[l.n], version))
        trs.append(self._table_row(('开始时间','Test Start Time')[l.n], f'{execStartTime}'))
        trs.append(self._table_row(('结束时间','Test End Time')[l.n], f'{execEndTime}'))
        trs.append(self._table_row(('耗时','Duration Of Testing')[l.n], f'{stats.test_duration:.3f}' + (' 秒',' Seconds')[l.n]))
        trs.append(self._table_row(('预备执行用例数量','number of cases plan to run')[l.n], ret['case_count_to_run'], 'primary'))
        trs.append(self._table_row(('实际执行用例数量','number of cases actually run')[l.n], ret['case_count'], 'primary'))
        trs.append(self._table_row(('通过','passed')[l.n], ret['case_pass'], 'success'))

        num = ret['case_fail']
        trs.append(self._table_row(('失败','failed')[l.n], num, 'danger' if num else None))
        errorNum += num
        
        num = ret['case_abort']
        trs.append(self._table_row(('异常','exception aborted')[l.n], num, 'abort' if num else None))
        errorNum += num

        trs.append(self._table_row(('阻塞','blocked')[l.n], blocked_num, 'warning' if blocked_num else None))
        
        num = ret['suite_setup_fail']
        trs.append(self._table_row(('套件初始化失败','suite setup failed')[l.n], num, 'danger' if num else None))
        errorNum += num
        
        num = ret['suite_teardown_fail']
        trs.append(self._table_row(('套件清除失败','suite teardown failed')[l.n], num, 'danger' if num else None))
        errorNum += num
        
        num = ret['case_setup_fail']
        trs.append(self._table_row(('用例初始化失败','cases setup failed')[l.n], num, 'danger' if num else None))
        errorNum += num
        
        num = ret['case_teardown_fail']
        trs.append(self._table_row(('用例清除失败','cases teardown failed')[l.n], num, 'danger' if num else None))
        errorNum += num

        if errorNum == 0 and blocked_num == 0:
            reportStatusText = ('全部通过','All Passed')[l.n]
            reportStatusClass = 'status_badge status-success'
        elif errorNum > 0:
            reportStatusText = ('存在失败/异常','Issues Detected')[l.n]
            reportStatusClass = 'status_badge status-danger'
        else:
            reportStatusText = ('存在阻塞','Blocked Cases')[l.n]
            reportStatusClass = 'status_badge status-warning'

        self.statusBadgeEle['class'] = reportStatusClass
        self.statusBadgeEle.add(reportStatusText)

        self.headerMetaEle.add(
            self._meta_item(('开始时间','Started At')[l.n], execStartTime),
            self._meta_item(('结束时间','Finished At')[l.n], execEndTime),
            self._meta_item(('总耗时','Duration')[l.n], f'{stats.test_duration:.3f}' + (' 秒',' Seconds')[l.n]),
            self._meta_item(('执行率','Execution Rate')[l.n], f'{execution_rate}%')
        )

        self.summaryCardsEle.add(
            self._summary_card(
                ('预备执行','Planned')[l.n],
                ret['case_count_to_run'],
                ('本次计划纳入执行的用例数','Cases included in this run.')[l.n],
                'primary'
            ),
            self._summary_card(
                ('实际执行','Executed')[l.n],
                ret['case_count'],
                f"{('执行率','Execution rate')[l.n]} {execution_rate}%",
                'primary'
            ),
            self._summary_card(
                ('通过','Passed')[l.n],
                ret['case_pass'],
                f"{('通过率','Pass rate')[l.n]} {pass_rate}%",
                'success'
            ),
            self._summary_card(
                ('失败','Failed')[l.n],
                ret['case_fail'],
                f"{('失败率','Failure rate')[l.n]} {fail_rate}%",
                'danger'
            ),
            self._summary_card(
                ('异常','Aborted')[l.n],
                ret['case_abort'],
                f"{('异常率','Abort rate')[l.n]} {abort_rate}%",
                'abort'
            ),
            self._summary_card(
                ('阻塞','Blocked')[l.n],
                blocked_num,
                f"{('阻塞率','Blocked rate')[l.n]} {blocked_rate}%",
                'warning' if blocked_num else 'neutral'
            )
        )

        self.ev['style'] = 'display:flex;' if errorNum else 'display:none;'

        # 添加结果统计表
        self.result_table.add(tbody(*trs))

        # 添加 结果柱状图
        add_barchar_item(
            ('用例通过','Cases Passed')[l.n],
            ret['case_pass'],
            pass_rate,
            '#04AA6D')

        add_barchar_item(
            ('用例失败','Cases Failed')[l.n],
            ret['case_fail'],
            fail_rate,
            '#bb4069')

        add_barchar_item(
            ('用例异常','Cases Aborted')[l.n],
            ret['case_abort'],
            abort_rate,
            '#9c27b0')


        add_barchar_item(
            ('用例阻塞','Cases Blocked')[l.n],
            blocked_num,
            blocked_rate,
            '#dcbdbd')


        # 产生文件
        htmlcontent = self.doc.render()

        timestamp = time.strftime('%Y%m%d_%H%M%S',time.localtime(stats.start_time))
        fileName = f'report_{timestamp}.html'
        reportPath = os.path.join('log',fileName)
        with open(reportPath,'w',encoding='utf8') as f:
            f.write(htmlcontent)

        if Settings.auto_open_report:
            try:
                my_os = platform.system().lower()
                if my_os == 'windows':
                    os.startfile(reportPath)
                elif my_os == 'darwin': # macOS
                    os.system(f'open {reportPath}')
            except:
                print(traceback.format_exc())

        #  with command line parameter report_url_prefix
        #  need to copy report from dir 'log' to 'reports'
        if Settings.report_url_prefix:
            os.makedirs('reports', exist_ok=True)
            cpTargetPath = os.path.join('reports',fileName)
            shutil.copyfile(reportPath, cpTargetPath)
            o1 = ('测试报告','test report')[l.n]
            print(f"{o1} : {Settings.report_url_prefix}/{fileName} \n")


    # def _findParentSuite(self,name):
    #     if name.endswith(os.path.sep):
    #         name = name[:-1]
        
    #     parentpath = os.path.dirname(name)

    #     # name 对应的 是用例根目录, 
    #     if  parentpath == '': 
    #         self._addSuiteDir(self.body,name)
    #         return None
        
    #     # rug 
    #     if parentpath not in self.suitepath2element:
    #         dirToCreate = []
    #         levels = parentpath.split(os.sep)
    #         cur = ''
    #         for level in levels:
    #             cur = os.path.join(cur,level)
            

    # 进入用例目录 或者 用例文件
    def enter_suite(self,name:str,suitetype): 
        _class = 'suite_'+suitetype

        enterInfo = ('进入目录','Enter Folder')[l.n] if suitetype == 'dir' \
                else ('进入文件','Enter File')[l.n]
        
        self.curEle = self.logDiv.add(
            div(                
                div(
                    span(enterInfo),
                    span(name),
                    _class='enter_suite'
                ),         
                _class=_class, id=f'{_class} {name}'
            )
        )
        self.curSuiteEle = self.curEle
        self.curSuiteFilePath = name

        self.suitepath2element[name] = self.curEle
             
    
    def enter_case(self, caseId ,name, case_className):       
        # 执行有结果后，要修改这个 self.curCaseLableEle ，比如 加上 PASS
        self.curCaseLableEle = span(('用例','Case')[l.n],_class='label caselabel')

        # folder_body 是折叠区 内容部分，可以隐藏
        self.curCaseBodyEle = div(
            span(f'{self.curSuiteFilePath}::{case_className}', _class='case_class_path') , 
            _class='folder_body')
        
        self.caseDurationSpan = span("", _class='duration')

        self.curCaseEle = self.curSuiteEle.add(
            div(
                div(
                    self.curCaseLableEle,
                    span(name, _class='casename'),
                    span(datetime.now().strftime('%m-%d %H:%M:%S'), _class='executetime'),
                    self.caseDurationSpan,
                    _class='folder_header'
                ),
                self.curCaseBodyEle ,
                _class='case',id=f'case_{caseId:08}'
               )
        )
        self.curEle = self.curCaseBodyEle

    def leave_case(self, caseId, duration):
        self.caseDurationSpan += f"{round(duration,1)}s"
    
    def case_steps(self,name):          
        self.stepsDurationSpan = span("", _class='duration')
        ele = div(
                div(
                    span(('测试步骤','Test Steps')[l.n],_class='label'),
                    self.stepsDurationSpan,
                    _class="flow-space-between",
                ),            
            _class='test_steps',id='test_steps '+name)    
        
        self.curEle = self.curCaseBodyEle.add(ele)

    
    # def case_pass(self, case, caseId, name): 
    #     self.curCaseEle['class'] += ' pass'
    #     self.curCaseLableEle += ' PASS'
    
    # def case_fail(self, case, caseId, name, e, stacktrace):
        
    #     self.curCaseEle['class'] += ' fail'
    #     self.curCaseLableEle += ' FAIL'

    #     self.curEle += div(f'{e} \n{stacktrace}', _class='info error-info')
        
    
    # def case_abort(self, case, caseId, name, e, stacktrace):
        
    #     self.curCaseEle['class'] += ' abort'
    #     self.curCaseLableEle += ' ABORT'

    #     self.curEle += div(f'{e} \n{stacktrace}', _class='info error-info')


    def case_result(self, case):
        if case.execRet == 'pass':
            self.curCaseEle['class'] += ' pass'
            self.curCaseLableEle += f" {('通过','PASS')[l.n]}"

        elif case.execRet == 'fail':
            self.curCaseEle['class'] += ' fail'
            self.curCaseLableEle += f" {('失败','FAIL')[l.n]}"
            self.curEle += div(f'{case.stacktrace}', _class='info error-info')
            
        elif case.execRet == 'abort':                
            self.curCaseEle['class'] += ' abort'
            self.curCaseLableEle += f" {('异常','ABORT')[l.n]}"

            self.curEle += div(f'{case.stacktrace}', _class='info abort-info')

        self.stepsDurationSpan += f"{round(case._steps_duration,1)}s"
            
    # utype 可能是 suite  case  case_default
    def setup_begin(self,name, utype): 
        
        _class = f'{utype}_setup setup'

        self.setupDurationSpan = span("", _class='duration')
                     
        # 套件 setup
        if utype.startswith('suite_'):
            
            # folder_body 是折叠区 内容部分，可以隐藏
            suiteHeaderEle = div(
                span(('套件初始化','Suite Setup')[l.n]),
                span(''),  #span(name),
                span(datetime.now().strftime('%m-%d %H:%M:%S'), _class='executetime'),
                self.setupDurationSpan,
                _class='folder_header')
            
            self.curSuiteHeaderEle = suiteHeaderEle
            
            stBodyEle = self.curEle = div(_class='folder_body')
            
            self.curSetupEle = div(
                suiteHeaderEle,
                stBodyEle,
                _class=_class,
                id=f'{_class} {name}')   

            self.curSuiteEle.add(self.curSetupEle)  

        # 用例 setup
        else:
            
            self.curSetupEle = self.curEle = div(
                div(
                    span(('用例初始化','Case Setup')[l.n],_class='label'),
                    self.setupDurationSpan,
                    _class="flow-space-between",
                ),
                _class=_class,
                id=f'{_class} {name}')   

            self.curCaseBodyEle.add(self.curSetupEle)
            self.curEle['class'] += ' case_st_lable'
    
            
    # utype 可能是 suite  case  case_default
    def setup_end(self, name, utype, duration): 

        self.setupDurationSpan += f"{round(duration,1)}s"



        
    # utype 可能是 suite  case  case_default
    def teardown_begin(self,name, utype): 

        _class = f'{utype}_teardown teardown'

        self.teardownDurationSpan = span("", _class='duration')

        # 套件 teardown
        if utype.startswith('suite_'):    

            # 是套件目录的清除，创建新的 curSuiteEle
            if utype == 'suite_dir':
                        
                self.curEle = self.logDiv.add(
                    div(                
                        div(
                            span(('离开目录','Leave Folder')[l.n] ),
                            span(name),
                            _class='leave_suite'
                        ),         
                        _class="suite_dir", id=f'{_class} {name}'
                    )
                )
                self.curSuiteEle = self.curEle
            
            # folder_body 是折叠区 内容部分，可以隐藏
            suiteHeaderEle = div(
                span(('套件清除','Suite Teardown')[l.n]),
                span(''),  #span(name),
                span(datetime.now().strftime('%m-%d %H:%M:%S'), _class='executetime'),
                self.teardownDurationSpan,
                _class='folder_header')
            
            stBodyEle = self.curEle = div(_class='folder_body')
            
            self.curTeardownEle = div(
                suiteHeaderEle,
                stBodyEle,
                _class=_class,
                id=f'{_class} {name}')   

            self.curSuiteEle.add(self.curTeardownEle)

        # 用例 teardown
        else:            
            self.curTeardownEle = self.curEle = div(                
                div(
                    span(('用例清除','Case Teardown')[l.n],_class='label'),
                    self.teardownDurationSpan,
                    _class="flow-space-between",
                ),
                _class=_class,
                id=f'{_class} {name}')       

            self.curCaseBodyEle.add(self.curTeardownEle)
            self.curEle['class'] += ' case_st_lable'

    # utype 可能是 suite  case  case_default
    def teardown_end(self, name, utype, duration): 
        self.teardownDurationSpan += f"{round(duration,1)}s"

    
    def setup_fail(self,name, utype, e, stacktrace):  
        self.curSetupEle['class'] += ' fail'
        self.curEle += div(f'{utype} setup fail | {e} \n{stacktrace}', _class='info error-info')
    
    def teardown_fail(self,name, utype, e, stacktrace):           
        self.curTeardownEle['class'] += ' fail'
        self.curEle += div(f'{utype} teardown fail | {e} \n{stacktrace}', _class='info error-info')

    def info(self, msg):
        msg = f'{msg}'
        if self.curEle is None:
            return

        self.curEle += div(msg, _class='info')


    def step(self,stepNo,desc):
        if self.curEle is None:
            return

        self.curEle += div(span(f'{("步骤","Step")[l.n]} #{stepNo}', _class='tag'), span(desc), _class='case_step')

    def checkpoint_pass(self, desc):
        if self.curEle is None:
            return

        self.curEle += div(span(f'{("检查点通过","Checkpoint PASS")[l.n]}', _class='tag'), 
                           span(desc, _class='paragraph' ), 
                           _class='checkpoint_pass')
        
    def checkpoint_fail(self, desc, compaireInfo):
        if self.curEle is None:
            return

        self.curEle += div(span(f'{("检查点失败","Checkpoint FAIL")[l.n]}', _class='tag'), 
                           span(f"{desc}\n\n{compaireInfo}" , _class='paragraph' ), 
                           _class='checkpoint_fail')


    def log_img(self,imgPath: str, width: str = None):
        if self.curEle is None:
            return

        self.curEle += div(img(src=imgPath, width= 'aa' if width is None else width, _class='screenshot' ))



from .signal import signal

signal.register([
    stats,
    ConsoleLogger(), 
    TextLogger(), 
    HtmlLogger()])


