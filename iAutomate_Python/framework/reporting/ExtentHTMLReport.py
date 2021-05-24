from framework import Status
import base64

__author__ = "Aniruddha Daryapurkar"
__email__ = "Aniruddha.Daryapurkar@Xoriant.Com"
__version__ = "1.0"

import datetime
import io
import sys
import re
from xml.sax import saxutils


class Template_mixin(object):
    """
    Define a HTML template for report customization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    # STATUS = {
    #     0: 'pass',
    #     1: 'fail',
    #     2: 'error',
    #     3: 'skip',
    #     4: 'pending',
    # }
    STATUS = {
        'Pass': 'pass',
        'Fail': 'fail',
        'Error': 'error',
        'Skip': 'skip',
        'Pending': 'pending'
    }

    DEFAULT_TITLE = 'AX-360 Report'
    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""
    <!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'/>
    <meta name='description' content=''/>
    <meta name='robots' content='noodp, noydir'/>
    <meta name='viewport' content='width=device-width, initial-scale=1'/>
    <meta id="timeStampFormat" name="timeStampFormat" content='MMM d, yyyy hh:mm:ss a'/>

    <link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600' rel='stylesheet' type='text/css'>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

    <link href='http://extentreports.com/resx/dist/css/extent.css' type='text/css' rel='stylesheet'/>

    <title>%(title)s - TestReport</title>
    %(stylesheet)s

</head>

<body class='extent standard default hide-overflow dark'>
<div id='theme-selector' alt='' title=''>
    <span><i class='material-icons'>desktop_windows</i></span>
</div>
%(heading)s

<div class='container'>
    %(report)s
    %(dashboard_view)s
</div>

</body>
%(script_js)s
</html>
"""
    # variables: (title, generator, stylesheet, heading, heading, ending)

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    NAV = """
    <nav>
    <div class="nav-wrapper">
        <a href="#!" class="brand-logo blue darken-3">Extent</a>

        <!-- slideout menu -->
        <ul id='slide-out' class='side-nav fixed hide-on-med-and-down'>
            <li class='waves-effect active'><a href='#!' view='test-view'
                                               onclick="configureView(0);chartsView('test');"><i class='material-icons'>dashboard</i></a>
            </li>
            <!-- <li class='waves-effect'><a href='#!' view='category-view' onclick="configureView(1)"><i
                    class='material-icons'>label_outline</i></a></li>
            <li class='waves-effect'><a href='#!' onclick="configureView(-1);chartsView('dashboard');"
                                        view='dashboard-view'><i class='material-icons'>track_changes</i></a></li> -->
        </ul>

        <!-- report name -->
        <span class='report-name'>Test Report: %(title)s</span>

        <!-- report headline -->
        <span class='report-headline'></span>

        <!-- nav-right -->
        <ul id='nav-mobile' class='right hide-on-med-and-down nav-right'>
            <li>
                <a href='#!'>
                    <span class='label suite-start-time blue darken-3'>Start_time: %(start_time)s</span>
                </a>
            </li>
            <li>
                <a href='#!'>
                    <span class='label blue darken-3'>Duration: %(duration)s </span>
                </a>
            </li>
        </ul>
    </div>
</nav>
    """

    TEST_VIEW = """
    <div id='test-view' class='view'>

        %(control_section)s

        %(view_charts)s
        %(test_list)s

        <div class='subview-right left'>
            <div class='view-summary'>
                <h5 class='test-name'></h5>

                <div id='step-filters' class="right">
                    <span class="blue-text" status="info" alt="info" title="info"><i
                            class="material-icons">info_outline</i></span>
                    <span class="green-text" status="pass" alt="pass" title="pass"><i class="material-icons">check_circle</i></span>
                    <span class="red-text" status="fail" alt="fail" title="fail"><i
                            class="material-icons">cancel</i></span>
                    <span class="red-text text-darken-4" status="fatal" alt="fatal" title="fatal"><i
                            class="material-icons">cancel</i></span>
                    <span class="pink-text text-lighten-1" status="error" alt="error" title="error"><i
                            class="material-icons">error</i></span>
                    <span class="orange-text" alt="warning" status="warning" title="warning"><i
                            class="material-icons">warning</i></span>
                    <span class="teal-text" status="skip" alt="skip" title="skip"><i
                            class="material-icons">redo</i></span>
                    <span status="clear" alt="Clear filters" title="Clear filters"><i
                            class="material-icons">clear</i></span>
                </div>
            </div>
        </div>
    </div>
    %(category_view)s

"""
    CONTROL_SECTION = """
    <section id='controls'>
            <div class='controls grey lighten-4'>
                <!-- test toggle -->
                <div class='chip transparent'>
                    <a class='dropdown-button tests-toggle' data-activates='tests-toggle' data-constrainwidth='true'
                       data-beloworigin='true' data-hover='true' href='#'>
                        <i class='material-icons'>warning</i> Status
                    </a>
                    <ul id='tests-toggle' class='dropdown-content'>
                        <li status='pass'><a href='#!'>Pass <i class='material-icons green-text'>check_circle</i></a></li>
                        <li status='fail'><a href='#!'>Fail <i class='material-icons red-text'>cancel</i></a></li>
                        <li status='error'><a href='#!'>Error <i class='material-icons red-text'>cancel</i></a></li>
                        <li status="skip"><a href="#!">Skip <i class="material-icons cyan-text">redo</i></a></li>
                        <li class='divider'></li>
                        <li status='clear' clear='true'><a href='#!'>Clear Filters <i
                                class='material-icons'>clear</i></a></li>
                    </ul>
                </div>
                <!-- test toggle -->

                <!-- category toggle -->
                <div class='chip transparent hide'>
                    <a class='dropdown-button category-toggle' data-activates='category-toggle'
                       data-constrainwidth='false' data-beloworigin='true' data-hover='true' href='#'>
                        <i class='material-icons'>local_offer</i> Category
                    </a>
                    <ul id='category-toggle' class='dropdown-content'>
                        %(suite_name)s
                        <li class='divider'></li>
                        <li class='clear'><a href='#!' clear='true'>Clear Filters</a></li>
                    </ul>
                </div>
                <!-- category toggle -->

                <!-- clear filters -->
                <div class='chip transparent hide'>
                    <a class='' id='clear-filters' alt='Clear Filters' title='Clear Filters'>
                        <i class='material-icons'>close</i> Clear
                    </a>
                </div>
                <!-- clear filters -->

                <!-- enable dashboard -->
                <div id='toggle-test-view-charts' class='chip transparent'>
                    <a class='pink-text' id='enable-dashboard' alt='Enable Dashboard' title='Enable Dashboard'>
                        <i class='material-icons'>track_changes</i> Dashboard
                    </a>
                </div>
                <!-- enable dashboard -->

                <!-- search -->
                <div class='chip transparent' alt='Search Tests' title='Search Tests'>
                    <a href="#" class='search-div'>
                        <i class='material-icons'>search</i> Search
                    </a>

                    <div class='input-field left hide'>
                        <input style="color: red" id='search-tests' type='text' class='validate browser-default'
                               placeholder='Search Tests...'>
                    </div>

                </div>
                <!-- search -->
            </div>
        </section>
    """
    SECTION_SUIT_NAME = """
    <li><a href='#'>%(group_name)s</a></li>
    """

    VIEW_CHARTS = """
    <div id='test-view-charts' class='subview-full'>
            <div id='test-view-charts' class='subview-full'>
                <div id='charts-row' class='row nm-v nm-h'>
                    <div class='col s12 m6 l6 np-h'>
                        <div class='card-panel nm-v'>
                            <div class='left panel-name'>Tests</div>
                            <div class='chart-box'>
                                <canvas id='parent-analysis' width='100' height='80'></canvas>
                            </div>
                            <div class='block text-small'>
                                <span class='tooltipped' data-position='top'><span class='strong'>%(pass_count)s</span> test(s) passed</span>
                                <span class='tooltipped' data-position='top'><span class='strong'>%(fail_count)s</span> test(s) failed</span>
                                <span class='strong tooltipped' data-position='top'>%(error_count)s</span> test(s) errored
                            </div>
                            <div class='block text-small'>
                                <span class='strong tooltipped' data-position='top'>%(skip_count)s</span> test(s) skipped
                                <span class='strong tooltipped' data-position='top'>%(pending_count)s</span> test(s) pending
                            </div>
                        </div>
                    </div>

                    <div class='col s12 m6 l6 np-h'>
                        <div class='card-panel nm-v'>
                            <div class='left panel-name'>Groups</div>
                            <div class='chart-box'>
                                <canvas id='child-analysis' width='100' height='80'></canvas>
                            </div>
                            <div class='block text-small'>
                                <span id="pass_suites" class='tooltipped' data-position='top'>%(pass_group_count)s</span> group(s) passed
                                <span id="fail_suites" class='tooltipped' data-position='top'>%(fail_group_count)s</span> group(s) failed
                                <span id="error_suites" class='tooltipped' data-position='top'>%(error_group_count)s</span> group(s) errored
                            </div>
                            <div class='block text-small'>
                                <span id="skip_suites" class='tooltipped' data-position='top'>%(skip_group_count)s</span> group(s) skipped
                                <span id="pending_suites" class='tooltipped' data-position='top'>%(pending_group_count)s</span> group(s) pending
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """

    SUBVIEW_LEFT = """
    <div class='subview-left left'>

            <div class='view-summary'>
                <h5>Groups</h5>
                <ul id='test-collection' class='test-collection'>
                %(groups_collection)s
                </ul>
            </div>
    </div>            
    """

    TEST_COLLECTION = """
    %(li_test_active)s
    <div class='test-heading'>
        <span class='test-name'>%(desc)s</span>
        <span class='test-time'>desc: %(doc)s </span>
        %(status_span)s
    </div>
    <div class='test-content hide'>
        <div class='test-desc'>Pass: %(Pass)s ;
                                Fail: %(fail)s ;
                                Error: %(error)s ;
                                Skip: %(skip)s ;
                                Pending: %(pending)s ;
        </div>
        <div class='test-attributes'>
            <div class='category-list'>
                <span class='category label white-text'>%(desc)s</span>
            </div>
        </div>
        <ul class='collapsible node-list' data-collapsible='accordion'>
            %(test_collection_ul_list)s
        </ul>
    </div>
    """
    TEST_COLLECTION_UL_LIST = """
            %(node_level)s
            <div class='collapsible-header'>
                <div class='node-name'>%(desc)s</div>
                <span class='node-time'>desc: %(doc)s</span>
                %(status_span)s
            </div>
            <div class='collapsible-body'>
                <div class='category-list right'>
                    <span class='category label white-text'>%(desc)s</span>
                </div>
                <div class='node-steps'>
                    <table class='bordered table-results'>
                        <thead>
                        <tr>
                            <th>Status</th>
                            <th>Identity</th>
                            <th>Details</th>
                        </tr>
                        </thead>
                        <tbody>
                        %(t_body)s
                        </tbody>
                    </table>
                 </div>
             </div>
            </li>
    """
    TBODY = """
        <tr class='info' status='info'>
            <td class='status info' title='info' alt='info'><i
                    class='material-icons'>low_priority</i></td>
            <td class='timestamp'>stdo</td>
            <td style="white-space:pre-wrap;word-break:break-all">%(script)s</td>
        </tr>
        <tr class='info' status='info'>
            <td class='status info' title='info' alt='info'><i
                    class='material-icons'>low_priority</i></td>
            <td class='timestamp'>screenshot</td>
            <td class='step-details'>%(images)s
            </td>
        </tr>
    """
    CATEGORY_VIEW = """
    <div id='category-view' class='view hide'>
        <section id='controls'>
            <div class='controls grey lighten-4'>
                <!-- search -->
                <div class='chip transparent' alt='Search Tests' title='Search Tests'>
                    <a href="#" class='search-div'>
                        <i class='material-icons'>search</i> Search
                    </a>

                    <div class='input-field left hide'>
                        <input tyle="color: red;" id='search-tests' type='text'
                               class='validate browser-default'
                               placeholder='Search Tests...'>
                    </div>

                </div>
                <!-- search -->
            </div>
        </section>

        <div class='subview-left left'>

            <div class='view-summary'>
                <h5>Categories</h5>
                <ul id='category-collection' class='category-collection'>

                    <li class='category displayed active'>
                        <div class='category-heading'>
                            <span class='category-name'>All Suites</span>
                            <span class='category-status right'>
                                <span class='label pass'>%(Pass)s </span>
                                <span class='label fail'>%(fail)s</span>
                            </span>
                        </div>
                        <div class='category-content hide'>
                            <div class='category-status-counts'>
                                <span class='label green accent-4 white-text'>Passed: %(Pass)s</span>
                                <span class='label red lighten-1 white-text'>Failed: %(fail)s</span>
                                <span class='label blue lighten-1 white-text'>Errored: %(error)s</span>
                                <span class="label yellow darken-2 white-text">Skipped: </span>
                                <span class="label yellow darken-2 white-text">Pending: </span>
                            </div>

                            <div class='category-tests'>
                                <table class='bordered table-results'>
                                    <thead>
                                    <tr>
                                        <th>Timestamp</th>
                                        <th>TestName</th>
                                        <th>Status</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    %(category_tbody)s
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </li>
                    %(category_active)s
                <div class='subview-right left'>
            <div class='view-summary'>
                <h5 class='category-name'></h5>
            </div>
        </div>
    </div>


    """
    CATEGORY_TBODY = """
    <tr style="border: 1px solid #49cc90; background-color: rgba(73, 204, 144, .1)">
        <td>%(start_time)s</td>
        <td class='linked' test-id='%(name)s_%(cid)s'>%(desc)s</td>
        <td>%(category_tbody_td)s</td>
    </tr>
    <tr>
        <td></td>
        <td class='linked' test-id='暂未处理'></td>
        <td>%(category_tbody_td)s</td>
    </tr>

    """

    CATEGORY_ACTIVE = """
    <li class='category displayed active'>
        <div class='category-heading'>
            <span class='category-name'>%(desc)s</span>
            <span class='category-status right'>
                <span class='label pass'>%(Pass)s </span>
                <span class='label fail'>%(fail)s</span>
                <span class='label fail'>%(error)s</span>
                <span class='label fail'>%(skip)s</span>
            </span>
        </div>
        <div class='category-content hide'>
            <div class='category-status-counts'>
                <span class='label green accent-4 white-text'>Passed: %(Pass)s</span>
                <span class='label red lighten-1 white-text'>Failed: %(fail)s</span>
                <span class='label blue lighten-1 white-text'>Errored: %(error)s</span>
                <span class='label blue lighten-1 white-text'>Skipped: %(skip)s</span>
                <span class='label blue lighten-1 white-text'>Pending: %(pending)s</span>
            </div>

            <div class='category-tests'>
                <table class='bordered table-results'>
                    <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>TestName</th>
                        <th>Status</th>
                    </tr>
                    </thead>
                    <tbody>

                    </tbody>
                </table>
            </div>
        </div>
    </li>
    """
    DASHBOARD_VIEW = """
    <div id='dashboard-view' class='view hide'>
        <div class='card-panel transparent np-v'>
            <h5>Dashboard</h5>

            <div class='row'>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Pass
                        <div class='panel-lead'>%(Pass)s</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Fail
                        <div class='panel-lead'>%(fail)s</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Error
                        <div class='panel-lead'>%(error)s</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Skip
                        <div class='panel-lead'></div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Start
                        <div class='panel-lead'>%(start_time)s</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Time Taken
                        <div class='panel-lead'>%(duration)s seconds</div>
                    </div>
                </div>
                <div class='col s4'>
                    <div class='card-panel'>
                        <span class='right label cyan white-text'>Categories</span>
                        <p>&nbsp;</p>
                        <table>
                            <tr>
                                <th>Name</th>
                                <th>Passed</th>
                                <th>Failed</th>
                                <th>Errored</th>
                                <th>Skipped</th>
                            </tr>
                            <tr>
                                <td>All Suites</td>
                                <td class="pass">%(Pass)s</td>
                                <td class="fail">%(fail)s</td>
                                <td class="error">%(error)s</td>
                                <td class="skip"></td>
                            </tr>

                                <tr>
                                    <td id="unknown"></td>
                                    <td class="pass"></td>
                                    <td class="fail"></td>
                                    <td class="error"></td>
                                    <td class="skip"></td>
                                </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    SCRIPT_JS = """
    <script>
        var test_groups_pass = %(grouppass)s;


        var statusGroup = {
            passParent: %(testpass)s,
            failParent: %(testfail)s,
            fatalParent: 0,
            errorParent: %(testerror)s,
            warningParent: 0,
            skipParent: %(testskip)s,
            pendingParent: %(testpending)s,
            exceptionsParent: 0,

            passChild: test_groups_pass,
            failChild: %(groupfail)s,
            fatalChild: 0,
            errorChild: %(grouperror)s,
            warningChild: 0,
            skipChild: %(groupskip)s,
            pendingChild: %(grouppending)s,
            infoChild: 0,
            exceptionsChild: 0,

            passGrandChild: 0,
            failGrandChild: 0,
            fatalGrandChild: 0,
            errorGrandChild: 0,
            warningGrandChild: 0,
            skipGrandChild: 0,
            infoGrandChild: 0,
            exceptionsGrandChild: 0,
        };

    </script>

    <script src='http://extentreports.com/resx/dist/js/extent.js' type='text/javascript'></script>


    <script type='text/javascript'>
        $(window).off("keydown");
    </script>
    """
    STYLESHEET_TMPL = """
    <style type="text/css">
        .node.level-1 ul {
            display: none;
        }

        .node.level-1.active ul {
            display: block;
        }

        .card-panel.environment th:first-child {
            width: 30%;
        }
        .small_img{
            height: 180px; 
            width: 100px; 
            padding: 10px;
            float: left;
            background-repeat: no-repeat; 
            background-position: center center; 
            background-size: cover; 
          } 
        .black_overlay{ 
            display: none; 
            position: absolute; 
            top: 0%; 
            left: 0%; 
            width: 100%; 
            height: 100%; 
            background-color: white; 
            z-index:1001; 
            -moz-opacity: 0.8; 
            opacity:.80; 
            filter: alpha(opacity=80);  
        } 
        .big_img { 
            cursor: pointer;
            display: none; 
            position: absolute; 
            height: 650px;
            left:50%; 
            top: 50%;
            margin: -300px 0px 0px -200px;
            z-index:1002; 
            overflow: auto; 
        }
    </style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_ATTRIBUTE_TMPL = """
    <p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
"""  # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #

    REPORT_TMPL = """
<p id='show_detail_line'>Show
<a href='javascript:showCase(0)'>Summary</a>
<a href='javascript:showCase(1)'>Failed</a>
<a href='javascript:showCase(2)'>All</a>
</p>
<table id='result_table'>
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>Test Group/Test case</td>
    <td>Count</td>
    <td>Pass</td>
    <td>Fail</td>
    <td>Error</td>
    <td>View</td>
    <td>Screenshot</td>
</tr>
%(test_list)s
<tr id='total_row'>
    <td>Total</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>

</tr>
</table>
"""  # variables: (test_list, count, Pass, fail, error)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
    <td>%(desc)s</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td><a href="javascript:showClassDetail('%(cid)s',%(count)s)">Detail</a></td>
    <td>&nbsp;</td>

</tr>
"""  # variables: (style, desc, count, Pass, fail, error, cid)

    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a>

    <div id='div_%(tid)s' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->

    </td>
    <td align='center'>
    %(images)s
    </td>
</tr>
"""  # variables: (tid, Class, style, desc, status)
    REPORT_IMAGE = """
        <img src="%(screenshot)s" style= onclick="document.getElementById('light_%(screenshot_id)s').style.display ='block';document.getElementById('fade_%(screenshot_id)s').style.display='block'"/>
        """

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>%(status)s</td>
</tr>
"""  # variables: (tid, Class, style, desc, status)
    REPORT_TEST_OUTPUT_TMPL = r"""
%(output)s
"""  # variables: (id, output)
    REPORT_TEST_OUTPUT_IMAGE = r""" 
%(screenshot)s
"""
    REPORT_TEST_OUTPUT_CASEID = r"""
%(case_id)s
"""
    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""


# -------------------- The end of the Template class -------------------


class _Result:
    test_pass_count = 0
    test_fail_count = 0
    test_error_count = 0
    test_pending_count = 0
    test_skip_count = 0

    group_pass_count = 0
    group_fail_count = 0
    group_error_count = 0
    group_skip_count = 0
    group_pending_count = 0

    result = []
    g_result = {}
    group_test_status_counts = {}

    def __init__(self, test_suite):
        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )

        for group in test_suite.groups:
            if group.status == Status.PASS:
                self.group_pass_count += 1
            if group.status == Status.FAIL:
                self.group_fail_count += 1
            if group.status == Status.ERROR:
                self.group_error_count += 1
            if group.status == Status.SKIP:
                self.group_skip_count += 1
            if group.status == Status.PENDING:
                self.group_pending_count += 1

            self.g_result[group.name] = group.status
            self.group_test_status_counts[group.name] = group.test_status_counts

            for test in group.tests:
                if test.status == Status.PASS:
                    self.test_pass_count += 1
                if test.status == Status.FAIL:
                    self.test_fail_count += 1
                if test.status == Status.ERROR:
                    self.test_error_count += 1
                if test.status == Status.SKIP:
                    self.test_skip_count += 1
                if test.status == Status.PENDING:
                    self.test_pending_count += 1

                steps = [x['status'] + '-' + x['step'] + ' ' for x in test.result]
                tup = (test.status, test, '\n'.join(steps), '')

                self.result.append(tup)


class HTMLTestRunner(Template_mixin):
    """
    """
    stopTime = None

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.startTime = datetime.datetime.now()

    @staticmethod
    def sortResult(result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        groups = []
        for status, test, logs, stacktrace in result_list:
            # cls = t.__class__
            grp = test.group_name
            if not grp in rmap:
                rmap[grp] = []
                groups.append(grp)
            rmap[grp].append((status, test, logs, stacktrace))
        r = [(grp, rmap[grp]) for grp in groups]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        if result.test_pass_count:
            status.append('Pass %s' % result.test_pass_count)
        if result.test_fail_count:
            status.append('Failure %s' % result.test_fail_count)
        if result.test_error_count:
            status.append('Error %s' % result.test_error_count)
        if result.test_skip_count:
            status.append('Skip %s' % result.test_skip_count)
        if result.test_pending_count:
            status.append('Error %s' % result.test_pending_count)

        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [
            ('Start Time', startTime),
            ('Duration', duration),
            ('Status', status),
        ]

    def generateReport(self, suite):

        result = _Result(suite)

        report_attrs = self.getReportAttributes(result)  # This can be called just set startTime, EndTime and counts
        generator = 'AX-360 Generator %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        dashboard_view = self._generate_dashboardView(report_attrs, result)
        scriptJS = self._generate_script(result)

        output = self.HTML_TMPL % dict(
            title=saxutils.escape(self.title),
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
            dashboard_view=dashboard_view,
            script_js=scriptJS,
        )
        self.stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        # HEADING_ATTRIBUTE_TMPL

        startTime = ""
        duration = ""
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            startTime = value if name == "Start Time" else startTime
            duration = value if name == "Duration" else duration
        # Start Time、Duration、Status
        heading = self.NAV % dict(
            title=saxutils.escape(self.title),
            start_time=startTime,
            duration=duration,
            description=saxutils.escape(self.description),
        )
        return heading

    def _generate_script(self, result):
        scriptJS = self.SCRIPT_JS % dict(
            testpass=str(result.test_pass_count),
            testfail=str(result.test_fail_count),
            testerror=str(result.test_error_count),
            testskip=str(result.test_skip_count),
            testpending=str(result.test_pending_count),
            grouppass=str(result.group_pass_count),
            groupfail=str(result.group_fail_count),
            grouperror=str(result.group_error_count),
            groupskip=str(result.group_skip_count),
            grouppending=str(result.group_pending_count),
        )
        return scriptJS

    def _generate_dashboardView(self, report_attrs, result):
        a_lines = []
        startTime = ""
        duration = ""
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)
            startTime = value if name == "Start Time" else startTime
            duration = value if name == "Duration" else duration
        # to be checked
        dashboard_view = self.DASHBOARD_VIEW % dict(
            Pass=str(result.test_pass_count),
            fail=str(result.test_fail_count),
            error=str(result.test_error_count),
            start_time=startTime,
            duration=duration,
        )
        return dashboard_view

    def _generate_report(self, result):
        rows = []
        left_groups = []
        section_name = []
        categoryTbody = []
        categoryActive = []
        sortedResult = self.sortResult(result.result)
        for cid, (group_name, group_results) in enumerate(sortedResult):

            # format class description
            if group_name == "__main__":
                name = "__main__"
            else:
                name = "%s" % (group_name)  # module should be without classname because class is a test

            # doc = group_name.__doc__ and group_name.__doc__.split("\n")[0] or ""
            # desc = doc and '%s: %s' % (name, doc) or name
            # desc = doc and '%s' % (name) or name
            group_doc = name
            category_group_name = '%s' % (name) or name

            sectionName = self.SECTION_SUIT_NAME % dict(
                group_name=category_group_name,
            )
            section_name.append(sectionName)

            testCollectionUlList = []
            for tid, (status, test, logs, stacktrace) in enumerate(group_results):
                self._generate_report_test(rows, cid, tid, status, test, logs, stacktrace, testCollectionUlList)

            grp_status = result.g_result[group_name].lower()
            liTestActive = str(
                '<li class="test displayed active has-leaf %(grp_status)s" status="%(grp_status)s" bdd="true" test-id="' + category_group_name + '_' + str(
                    cid + 1) + '">') % dict(grp_status=grp_status)
            statusSpan = str('<span class="test-status right %(grp_status)s">%(grp_status)s</span>') % dict(
                grp_status=grp_status)
            nodeLevel = str(
                '<li class="node level-1 leaf %(grp_status)s" status="%(grp_status)s" test-id="' + category_group_name + '_' + str(
                    cid + 1) + '">') % dict(grp_status=grp_status)
            categoryTbodyTd = str('<span class="test-status %(grp_status)s">%(grp_status)s</span>') % dict(
                grp_status=grp_status)

            npass = result.group_test_status_counts[group_name][Status.PASS]
            nfail = result.group_test_status_counts[group_name][Status.FAIL]
            nerror = result.group_test_status_counts[group_name][Status.ERROR]
            nskip = result.group_test_status_counts[group_name][Status.SKIP]
            npending = result.group_test_status_counts[group_name][Status.PENDING]

            row1 = self.TEST_COLLECTION % dict(
                li_test_active=liTestActive,
                status_span=statusSpan,
                node_level=nodeLevel,
                desc=category_group_name,
                doc=group_doc,
                count=npass + nfail + nerror + nskip + npending,
                Pass=npass,
                fail=nfail,
                error=nerror,
                skip=nskip,
                pending=npending,
                test_collection_ul_list=''.join(testCollectionUlList),
                cid='c%s' % (cid + 1),
            )
            left_groups.append(row1)
            category_tbody = self.CATEGORY_TBODY % dict(
                name=name,
                desc=category_group_name,
                start_time=self.startTime,
                cid=cid,
                category_tbody_td=categoryTbodyTd,
            )
            categoryTbody.append(category_tbody)

            category_active = self.CATEGORY_ACTIVE % dict(
                desc=category_group_name,
                Pass=npass,
                fail=nfail,
                error=nerror,
                skip=nskip,
                pending=npending,
            )
            categoryActive.append(category_active)

        controlSection = self.CONTROL_SECTION % dict(
            suite_name=''.join(section_name)
        )
        # can be checked
        viewCharts = self.VIEW_CHARTS % dict(
            pass_count=str(result.test_pass_count),
            fail_count=str(result.test_fail_count),
            error_count=str(result.test_error_count),
            skip_count=str(result.test_skip_count),
            pending_count=str(result.test_pending_count),
            pass_group_count=str(result.group_pass_count),
            fail_group_count=str(result.group_fail_count),
            error_group_count=str(result.group_error_count),
            skip_group_count=str(result.group_skip_count),
            pending_group_count=str(result.group_pending_count),
        )
        subviewLeft = self.SUBVIEW_LEFT % dict(
            groups_collection=''.join(left_groups),
        )
        category_view = self.CATEGORY_VIEW % dict(
            Pass=str(result.test_pass_count),
            fail=str(result.test_fail_count),
            error=str(result.test_error_count),
            category_tbody=categoryTbody,
            category_active=categoryActive,
        )

        report = self.TEST_VIEW % dict(
            control_section=controlSection,
            view_charts=viewCharts,
            # test_list=''.join(rows),   not needed
            test_list=subviewLeft,
            count=str(result.test_pass_count + result.test_fail_count + result.test_error_count),
            Pass=str(result.test_pass_count),
            fail=str(result.test_fail_count),
            error=str(result.test_error_count),
            category_view=category_view,
        )
        return report

    def _generate_report_test(self, rows, cid, tid, status, test, logs, stacktrace, testCollectionUlList):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(logs or stacktrace)
        # tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)
        tid = (status == 'Pass' and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)
        # name = t.id().split('.')[-1]
        name = test.name
        # doc = t.shortDescription() or ""
        doc = test.__doc__
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.TBODY or self.REPORT_TEST_NO_OUTPUT_TMPL

        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(logs, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            # uo = o.decode('latin-1')
            uo = str(logs)
        else:
            uo = stacktrace
        if isinstance(stacktrace, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            # ue = e.decode('latin-1')
            ue = stacktrace
        else:
            ue = stacktrace

        # screenshot base64 can go here
        ssreg = re.compile(r'screenshot_.+?png')
        ss = ssreg.findall(uo)
        # ss = ';'.join(ss)
        imagesssss = HTMLTestRunner.__get_base64_from_screenshot_links(test)
        images = []
        for ima in imagesssss:
            image = self.REPORT_IMAGE % dict(
                screenshot_id=ima[0],
                screenshot='data:image/png;base64,' + ima[1]
            )
            images.append(image)
        images = ''.join(images)

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id=cid,
            # output=saxutils.escape(uo+ue),
            output=((uo + ue).replace("\n", "<br />")),
        )

        tBody = self.TBODY % dict(
            script=script,
            images=images,
        )

        if status == "Pending":
            nodeLevel = '<li class="node level-1 leaf pending" status="pending" test-id="' + desc + '_' + str(
                tid) + '_' + str(cid + 1) + '">'
            statusSpan = '<span class="test-status right pending">pending</span>'
        elif status == "Skip":
            nodeLevel = '<li class="node level-1 leaf skip" status="skip" test-id="' + desc + '_' + str(
                tid) + '_' + str(cid + 1) + '">'
            statusSpan = '<span class="test-status right skip">skip</span>'
        elif status == "Fail":
            nodeLevel = '<li class="node level-1 leaf fail" status="fail" test-id="' + desc + '_' + str(
                tid) + '_' + str(cid + 1) + '">'
            statusSpan = '<span class="test-status right fail">fail</span>'
        elif status == "Error":
            nodeLevel = '<li class="node level-1 leaf error" status="error" test-id="' + desc + '_' + str(
                tid) + '_' + str(cid + 1) + '">'
            statusSpan = '<span class="test-status right error">error</span>'
        else:
            nodeLevel = '<li class="node level-1 leaf pass" status="pass" test-id="' + desc + '_' + str(
                tid) + '_' + str(cid + 1) + '">'
            statusSpan = '<span class="test-status right pass">pass</span>'

        tcll = self.TEST_COLLECTION_UL_LIST % dict(
            node_level=nodeLevel,
            status_span=statusSpan,
            desc=name,
            doc=doc,
            t_body=tBody,
        )

        testCollectionUlList.append(tcll)
        caseid = self.REPORT_TEST_OUTPUT_CASEID % dict(
            case_id=saxutils.escape(uo + ue)
        )
        row = tmpl % dict(
            tid=tid,
            Class=(status == "Pass" and 'hiddenRow' or 'none'),
            style=status == "Error" and 'errorCase' or (status == "Fail" and 'failCase' or 'none'),
            desc=desc,
            script=script,
            # image = image[image.find("image"):(int(image.find("png"))+3)],
            images=images,
            # caseid=caseid[caseid.find("case"):(int(caseid.find("case")) + 9)],
            caseid=name,
            status=self.STATUS[status],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL

    @staticmethod
    def __get_base64_from_screenshot_links(test):
        """
        :param test:
        :return:
        """
        paths = []
        for r in test.result:
            if r['snapshots']:
                paths.extend(r['snapshots'])
        base64images = []
        for path in paths:
            base64images.append((path, base64.b64encode(open(path, "rb").read()).decode()))
        return base64images
