import re,os,traceback
from .cfg import l, Settings
import argparse
from .product import version
from pathlib import Path
from typing import List

def merge_containing_paths(paths: List[str]) -> List[str]:
    """
    合并具有包含关系的路径，尽量保持原始路径的出现顺序。
    如果一个路径包含另一个路径，则保留更上层的那个。
    当冲突时，优先保留先出现的路径。
    """
    if not paths:
        return []

    # 将所有路径转换为 Path 对象（保持相对路径，不 resolve）
    path_objs = [Path(p) for p in paths]

    # 用于记录哪些索引的路径需要被保留
    to_keep = set(range(len(paths)))  # 初始全部保留

    # 从前往后遍历
    for i, current in enumerate(path_objs):
        if i not in to_keep:
            continue  # 已经被移除，不处理

        for j, other in enumerate(path_objs):
            if i == j or j not in to_keep:
                continue

            try:
                # 如果 other 是 current 的子路径 → 移除 other
                if other.is_relative_to(current):
                    to_keep.discard(j)
                # 如果 current 是 other 的子路径 → 移除当前 i（因为 other 先出现）
                elif current.is_relative_to(other):
                    to_keep.discard(i)
                    break  # 当前被移除，后续无需再比较
            except ValueError:
                # 不存在包含关系
                pass

    # 按原始顺序返回保留下来的路径（字符串形式）
    result = [paths[i] for i in sorted(to_keep)]
    return result



def tagExpressionGen(argstr):
    tagRules = []
    for part in argstr:
        # 有单引号，是表达式
        if "'" in part:
            rule = re.sub(r"'.+?'", lambda m :f'tagmatch({m.group(0)})' , part)
            tagRules.append(f'({rule})')
        # 是简单标签名
        else:
            rule = f"tagmatch('{part}')"
            tagRules.append(f'{rule}')
    return ' or '.join(tagRules)

def run() :
    
    print(f'''           
    *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *     
    *       hytest {version}            www.byhy.net      *
    *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    '''
    )


    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'hytest v{version}',
                        help=("显示版本号", 'display hytest version')[l.n])
    parser.add_argument('--lang', choices=['zh', 'en'],
                        help=("设置工具语言", 'set language')[l.n])
    parser.add_argument('--new', metavar='project_dir',
                        help=("创建新项目目录", "create a project folder")[l.n])
    parser.add_argument("file_or_dir", nargs='*', default=['cases'],
                        help=("用例目录或文件", "test case files or directories")[l.n])
    parser.add_argument("--loglevel", metavar='level_number', type=int, default=3,
                        help=("日志级别 0,1,2,3,4,5(数字越大，日志越详细)", "log level 0,1,2,3,4,5(bigger for more info)")[l.n])

    parser.add_argument('--auto_open_report', choices=['yes', 'no'], default='yes',
                        help=("测试结束不自动打开报告", "don't open report automatically after testing")[l.n])
    parser.add_argument("--report_title", metavar='report_title',
                        default=['测试报告','Test Report'][l.n],
                        help=['指定测试报告标题','set test report title'][l.n])
    parser.add_argument("--report_url_prefix", metavar='url_prefix',
                        default='',
                        help=['测试报告URL前缀','test report URL prefix'][l.n])

    parser.add_argument("--test", metavar='case_name', action='append', default=[],
                        help=("用例名过滤，支持通配符", "filter by case name")[l.n])
    parser.add_argument("--suite", metavar='suite_name', action='append', default=[],
                        help=("套件名过滤，支持通配符", "filter by suite name")[l.n])
    parser.add_argument("--tag", metavar='tag_expression', action='append', default=[],
                        help=("标签名过滤，支持通配符", "filter by tag name")[l.n])
    parser.add_argument("--tagnot", metavar='tag_expression', action='append', default=[],
                        help=("标签名反向过滤，支持通配符", "reverse filter by tag name")[l.n])
    parser.add_argument("-A", "--argfile", metavar='argument_file',
                        type=argparse.FileType('r', encoding='utf8'),
                        help=("使用参数文件", "use argument file")[l.n])
    parser.add_argument("-saic", "--set-ai-context", metavar='ai_context_file',
                        type=str,
                        help=("设置 AI Context 文件（比如 GEMINI.md）内容，加入hytest使用方法", "set AI context file(like GEMINI.md) by appending hytest guide")[l.n])

    args = parser.parse_args()

    # 有参数放在文件中，必须首先处理
    if args.argfile:
        fileArgs = [para for para in args.argfile.read().replace('\n',' ').split() if para]
        print(fileArgs)
        args = parser.parse_args(fileArgs,args)

    # 设置AI上下文内容
    if args.set_ai_context:
        ctxFile = args.set_ai_context
        ctxContent = ''
        
        if os.path.exists(ctxFile):
            with open(ctxFile, encoding='utf8') as f:
                ctxContent = f.read() + '\n\n'
               
            if '# hytest 自动化测试框架 简介' in ctxContent:   
                print(f'{ctxFile} {("里面已经包含了hytest资料", "already includes hytest guide.")[l.n]}')
                exit()

        hytestGuideFile = os.path.join(os.path.dirname(__file__), 'utils','hytest.md')   
        ctxContent += open(hytestGuideFile, encoding='utf8').read()

        with open(ctxFile, 'w', encoding='utf8') as f:
            f.write(ctxContent)

        print(f'{ctxFile} {("里面增加了hytest资料", "now includes hytest guide.")[l.n]}')
        exit()
        

    # 看命令行中是否设置了语言
    if args.lang:
        l.n = l.LANGS[args.lang]

    # 报告标题
    Settings.report_title = args.report_title

    # 测试结束后，是否自动打开测试报告
    Settings.auto_open_report = True if args.auto_open_report=='yes' else False

    # 测试结束后，要显示的测试报告的url前缀,比如： run.bat --report_url_prefix http://127.0.0.1
    # 可以本机启动http服务，比如：python -m http.server 80 --directory log
    # 方便 jenkins上查看
    Settings.report_url_prefix = args.report_url_prefix

    # 创建项目目录
    if args.new:
        projDir =  args.new
        if os.path.exists(projDir):
            print(f'{projDir} already exists！')
            exit(2)
        os.makedirs(f'{projDir}/cases')
        with open(f'{projDir}/cases/case1.py','w',encoding='utf8') as f:
            caseContent = [
'''class c1:
    name = '用例名称 - 0001'

    # 测试用例步骤
    def teststeps(self):
        ret = 1
        ''' ,

'''class c1:
    name = 'test case name - 0001'

    # test case steps
    def teststeps(self):...''',
    ][l.n]
            f.write(caseContent)

        exit()


    for f in args.file_or_dir:
        if not os.path.exists(f) :
            print(f' {f} {("不存在，工作目录为：","not exists, workding dir is:")[l.n]} {os.getcwd()}')
            exit(2)  #  '2' stands for no test cases to run
    
    # 确保 file_or_dir 里面不存在包含关系，比如 ['cases', 'cases/sub']，只保留 'cases'
    args.file_or_dir = merge_containing_paths(args.file_or_dir)
    # print('测试用例路径：', args.file_or_dir)



    # 同时执行log里面的初始化日志模块，注册signal的代码
    from .utils.log import LogLevel
    from .utils.runner import Collector, Runner

    LogLevel.level = args.loglevel
    # print('loglevel',LogLevel.level)


    # --tag "'冒烟测试' and 'UITest' or (not '快速' and 'fast')" --tag 白月 --tag 黑羽

    tag_include_expr = tagExpressionGen(args.tag)
    tag_exclude_expr = tagExpressionGen(args.tagnot)

    # print(tag_include_expr)
    # print(tag_exclude_expr)



    os.makedirs('log/imgs', exist_ok=True)

    try:
        Collector.run(
            file_or_dir=args.file_or_dir,
            suitename_filters=args.suite,
            casename_filters=args.test,
            tag_include_expr=tag_include_expr,
            tag_exclude_expr=tag_exclude_expr,
            )
    except:
        print(traceback.format_exc())
        print(('\n\n!! 搜集用例时发现代码错误，异常终止 !!\n\n', 
               '\n\n!! Collect Test Cases Exception Aborted !!\n\n')[l.n])
        exit(3)

    # exit(0)
    
    # 0 表示执行成功 , 1 表示有错误 ， 2 表示没有可以执行的用例
    result =  Runner.run()

    # keep 10 report files at most
    ReportFileNumber = 10
    import glob
    reportFiles = glob.glob('./log/report_*.html')
    fileNum = len(reportFiles)
    if fileNum >= ReportFileNumber:
        reportFiles.sort()
        for rf in reportFiles[:fileNum-ReportFileNumber]:
            try:
                os.remove(rf)
            except:...

    return result


if __name__ == '__main__':
    exit(run())