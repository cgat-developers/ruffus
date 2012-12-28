.. include:: ../../global.inc
.. _Simple_Tutorial_1st_step:
    
    * :ref:`Simple tutorial overview <Simple_Tutorial>` 

###################################################################
Step 1: An introduction to Ruffus pipelines
###################################################################

************************************
Overview
************************************

    .. raw:: html

        <svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0"
            width="731.3pt"
            height="83pt"
            viewBox="0 0 731.3 83">
          <defs id="defs3287">
            <marker refX="0" refY="0" orient="auto" id="Arrow2Mend" style="overflow:visible">
              <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="scale(-0.6,-0.6)" id="path4124" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
            </marker>
            <marker refX="0" refY="0" orient="auto" id="Arrow2Lend" style="overflow:visible">
              <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="matrix(-1.1,0,0,-1.1,-1.1,0)" id="path4118" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
            </marker>
            <marker refX="0" refY="0" orient="auto" id="Arrow1Lend" style="overflow:visible">
              <path d="M 0,0 5,-5 -12.5,0 5,5 0,0 z" transform="matrix(-0.8,0,0,-0.8,-10,0)" id="path4100" style="fill-rule:evenodd;stroke:#000000;stroke-width:1pt" />
            </marker>
            <marker refX="0" refY="0" orient="auto" id="Arrow2Mend-4" style="overflow:visible">
              <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="scale(-0.6,-0.6)" id="path4124-8" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
            </marker>
            <marker refX="0" refY="0" orient="auto" id="Arrow2Mend-1" style="overflow:visible">
              <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="scale(-0.6,-0.6)" id="path4124-1" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
            </marker>
            <marker refX="0" refY="0" orient="auto" id="Arrow2Mend-1-1" style="overflow:visible">
              <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="scale(-0.6,-0.6)" id="path4124-1-8" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
            </marker>
            <marker refX="0" refY="0" orient="auto" id="Arrow2Mend-1-2" style="overflow:visible">
              <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="scale(-0.6,-0.6)" id="path4124-1-7" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
            </marker>
            <marker refX="0" refY="0" orient="auto" id="Arrow2Mend-1-23" style="overflow:visible">
              <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="scale(-0.6,-0.6)" id="path4124-1-3" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
            </marker>
          </defs>
          <g transform="translate(-14.608261,-32.693481)" id="layer1">
            <rect width="89.826035" height="65.392792" x="21.063463" y="39.148708" id="rect3309" style="fill:#ffff00;fill-opacity:1;stroke:#ff0000;stroke-width:0.41040453" />
            <text x="64.540756" y="62.738293" id="text3311" xml:space="preserve" style="font-size:14px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="67.314194" y="62.738293" id="tspan3313" style="font-size:20px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;font-family:Arial;-inkscape-font-specification:Arial Bold">Starting </tspan><tspan x="64.540756" y="87.738297" id="tspan3315" style="font-size:20px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;font-family:Arial;-inkscape-font-specification:Arial Bold">Data</tspan></text>
            <text x="118.47811" y="104.62877" id="text4956" xml:space="preserve" style="font-size:21.02927971px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#ff0000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="118.47811" y="104.62877" id="tspan4958" style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;fill:#ff0000;font-family:Arial;-inkscape-font-specification:Arial Bold">task_1()</tspan></text>
            <text x="345.62097" y="104.98591" id="text4956-1" xml:space="preserve" style="font-size:21.02927971px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#ff0000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="345.62097" y="104.98591" id="tspan4958-7" style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;fill:#ff0000;font-family:Arial;-inkscape-font-specification:Arial Bold">task_2()</tspan></text>
            <text x="575.62097" y="103.03347" id="text4956-2" xml:space="preserve" style="font-size:21.02927971px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#ff0000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="575.62097" y="103.03347" id="tspan4958-3" style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;fill:#ff0000;font-family:Arial;-inkscape-font-specification:Arial Bold">task_3()</tspan></text>
            <path d="m 110.71429,72.362182 87.14285,0" id="path5080" style="fill:#ff0000;stroke:#ff0000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;marker-end:url(#Arrow2Mend-1)" />
            <rect width="131.88234" height="65.306244" x="206.10674" y="39.191959" id="rect3309-6" style="fill:#ffff00;fill-opacity:1;stroke:#ff0000;stroke-width:0.49695465" />
            <text x="273.11218" y="65.772057" id="text3311-2-2" xml:space="preserve" style="font-size:14px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="273.11218" y="65.772057" id="tspan3313-4-2" style="font-size:20px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;font-family:Arial;-inkscape-font-specification:Arial Bold">Intermediate</tspan><tspan x="273.11218" y="90.772057" id="tspan3315-5-1" style="font-size:20px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;font-family:Arial;-inkscape-font-specification:Arial Bold">Data 1</tspan></text>
            <path d="m 338.57143,72.362177 87.14285,0" id="path5080-9" style="fill:#ff0000;stroke:#ff0000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;marker-end:url(#Arrow2Mend-1)" />
            <rect width="131.88234" height="65.306244" x="433.96387" y="39.191959" id="rect3309-6-4" style="fill:#ffff00;fill-opacity:1;stroke:#ff0000;stroke-width:0.49695465" />
            <text x="500.96933" y="65.772057" id="text3311-2-2-1" xml:space="preserve" style="font-size:14px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="500.96933" y="65.772057" id="tspan3313-4-2-1" style="font-size:20px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;font-family:Arial;-inkscape-font-specification:Arial Bold">Intermediate</tspan><tspan x="500.96933" y="90.772057" id="tspan3315-5-1-3" style="font-size:20px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;font-family:Arial;-inkscape-font-specification:Arial Bold">Data 2</tspan></text>
            <path d="m 566.42857,72.362178 87.14285,0" id="path5080-9-8" style="fill:#ff0000;stroke:#ff0000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;marker-end:url(#Arrow2Mend-1)" />
            <flowRoot id="flowRoot5373" xml:space="preserve" style="font-size:14px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><flowRegion id="flowRegion5375"><rect width="56.42857" height="339.28571" x="214.28572" y="123.07647" id="rect5377" /></flowRegion><flowPara id="flowPara5379"></flowPara></flowRoot>    <rect width="74.861671" height="65.428436" x="664.61707" y="39.130863" id="rect3309-6-4-7" style="fill:#ffff00;fill-opacity:1;stroke:#ff0000;stroke-width:0.37476507" />
            <text x="700.25507" y="65.071579" id="text3311-2-8" xml:space="preserve" style="font-size:14px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="700.25507" y="65.071579" id="tspan3315-5-7" style="font-size:20px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;font-family:Arial;-inkscape-font-specification:Arial Bold">Final</tspan><tspan x="700.25507" y="90.071579" id="tspan5078" style="font-size:20px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;font-family:Arial;-inkscape-font-specification:Arial Bold">Result</tspan></text>
          </g>
        </svg>

    Computational pipelines transform your data in stages until the final result is produced. One easy way to understand pipelines is by imagining your data flowing across a series of pipes until it reaches its final destination. Even quite complicated processes can be simplified if we broke things down into simple stages. Of course, it helps if we can visualise the whole process.

    Ruffus is a way of automating the plumbing in your pipeline: You supply the python functions which perform the data transformation, and tell Ruffus how these pipeline ``task`` functions are connected up. Ruffus will make sure that the right data flows down your pipeline in the right way at the right time.

    
    .. note::
        
        Ruffus refers to each stage of your pipeline as a :term:`task`.

***************************************
A gentle introduction to Ruffus syntax
***************************************

    | Let us start with the usual "Hello World" programme.
    | We have the following two python functions which
      we would like to turn into an automatic pipeline:
      
    
        ::
        
            def first_task():
                print "Hello "
        
            def second_task():
                print "world"

    
    The simplest **Ruffus** pipeline would look like this:
    
        .. ::
        
            from ruffus import *
            
            def first_task():
                print "Hello "
        
            @follows(first_task)
            def second_task():
                print "world"
    
            pipeline_run([second_task])


    .. raw:: html

        <svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0"
            width="411pt"
            height="166pt"
            viewBox="0 0 411 166">
        <rect width="193.46577" height="153.25462" x="113.1341" y="6.25" id="rect3523-1" style="fill:#eeffcc" /><g transform="matrix(0.74399708,0,0,0.74399708,123.4741,7.2693622)" id="g6703" style="font-size:14px;font-family:monospace"><text x="0" y="14" id="text6705" xml:space="preserve"><tspan id="tspan6707" style="font-weight:bold;fill:#008000">from</tspan> <tspan id="tspan6709" style="font-weight:bold;fill:#0e84b5">ruffus</tspan> <tspan id="tspan6711" style="font-weight:bold;fill:#008000">import</tspan> <tspan id="tspan6713" style="fill:#303030">*</tspan></text>
        <text x="0" y="33" id="text6715" xml:space="preserve" />
        <text x="0" y="52" id="text6717" xml:space="preserve"><tspan id="tspan6719" style="font-weight:bold;fill:#008000">def</tspan> <tspan id="tspan6721" style="font-weight:bold;fill:#0060b0">first_task</tspan>():</text>
        <text x="0" y="71" id="text6723" xml:space="preserve">    <tspan id="tspan6725" style="font-weight:bold;fill:#008000">print</tspan> &quot;Hello &quot;</text>
        <text x="0" y="90" id="text6727" xml:space="preserve" />
        <text x="0" y="109" id="text6729" xml:space="preserve"><tspan id="tspan6731" style="font-weight:bold;fill:#505050">@follows</tspan>(first_task)</text>
        <text x="0" y="128" id="text6733" xml:space="preserve"><tspan id="tspan6735" style="font-weight:bold;fill:#008000">def</tspan> <tspan id="tspan6737" style="font-weight:bold;fill:#0060b0">second_task</tspan>():</text>
        <text x="0" y="147" id="text6739" xml:space="preserve">    <tspan id="tspan6741" style="font-weight:bold;fill:#008000">print</tspan> &quot;world&quot;</text>
        <text x="0" y="166" id="text6743" xml:space="preserve" />
        <text x="0" y="185" id="text6745" xml:space="preserve">pipeline_run([second_task])</text>
        <text x="0" y="204" id="text6747" xml:space="preserve" />
        </g><g transform="matrix(0,-1.0740862,0.50028548,0,83.609122,151.75772)" id="g3645-7" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1"><line x1="125.896" y1="53.333" x2="125.896" y2="15.667" id="line3647-4" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1" /><g id="g3649-0" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1"><line stroke-miterlimit="10" x1="125.896" y1="49.028" x2="125.896" y2="15.667" id="line3651-9" style="fill:#ff0000;stroke:#ff0000;stroke-miterlimit:10;stroke-opacity:1" /><g id="g3653-4" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1"><polygon points="128.888,48.153 125.897,53.333 122.905,48.153 " id="polygon3655-8" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1" /></g></g></g><path d="m 249.80886,84.752058 c 0,3.843158 -7.76261,6.959107 -17.33843,6.959107 h -97.44644 c -9.57593,0 -17.33855,-3.115949 -17.33855,-6.959107 l 0,0 c 0,-3.843212 7.76262,-6.959217 17.33855,-6.959217 h 97.44463 c 9.57588,0 17.34024,3.116005 17.34024,6.959217 l 0,0 z" id="path3671-8" style="opacity:0.2;fill:#00a14b" /><text x="5.7094913" y="19.39653" id="text3643-24" style="font-size:12.87146473px;fill:#ff0000;font-family:ArialMT">1. Input Ruffus</text>
        <path d="m 295.24733,142.14802 c 0,3.84316 -10.60785,6.95911 -23.6936,6.95911 H 138.38975 c -13.08581,0 -23.69366,-3.11595 -23.69366,-6.95911 l 0,0 c 0,-3.84321 10.60785,-6.95927 23.69366,-6.95927 h 133.16146 c 13.08587,0 23.69612,3.11606 23.69612,6.95927 l 0,0 z" id="path3671-9" style="fill:none;stroke:#ff0000;stroke-width:1.07262194;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" /><path d="m 254.65378,15.578563 c 0,3.87736 -8.2265,7.02106 -18.37473,7.02106 H 133.00887 c -10.14824,0 -18.37468,-3.1437 -18.37468,-7.02106 l 0,0 c 0,-3.87737 8.22644,-7.0210708 18.37468,-7.0210708 h 103.26837 c 10.14813,0 18.37654,3.1437008 18.37654,7.0210708 l 0,0 z" id="path3671-9-8" style="fill:none;stroke:#ff0000;stroke-width:0.94877779;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" /><g transform="matrix(0,-1.0740862,0.50028548,0,83.609122,279.27887)" id="g3645-5" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1"><line x1="125.896" y1="53.333" x2="125.896" y2="15.667" id="line3647-0" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1" /><g id="g3649-2" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1"><line stroke-miterlimit="10" x1="125.896" y1="49.028" x2="125.896" y2="15.667" id="line3651-8" style="fill:#ff0000;stroke:#ff0000;stroke-miterlimit:10;stroke-opacity:1" /><g id="g3653-6" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1"><polygon points="128.888,48.153 125.897,53.333 122.905,48.153 " id="polygon3655-0" style="fill:#ff0000;stroke:#ff0000;stroke-opacity:1" /></g></g></g><text x="5.7094913" y="146.74339" id="text3643-2" style="font-size:12.87146473px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;fill:#ff0000;font-family:Arial;-inkscape-font-specification:Arial">3.Run pipeline</text>
        <line style="fill:#ff0000;stroke:#ff0000;stroke-width:0.73304141;stroke-opacity:1" id="line3647-8" y2="83.510956" x2="78.575699" y1="83.510956" x1="97.419533" /><g transform="matrix(0,-1.0740862,0.50028548,0,70.737661,218.73401)" id="g3649-6" style="fill:#008000;stroke:#008000;stroke-opacity:1"><line style="fill:#008000;stroke:#008000;stroke-miterlimit:10;stroke-opacity:1" id="line3651-5" y2="15.667" x2="125.896" y1="49.028" x1="125.896" stroke-miterlimit="10" /><g id="g3653-0" style="fill:#008000;stroke:#008000;stroke-opacity:1"><polygon points="125.897,53.333 122.905,48.153 128.888,48.153 " id="polygon3655-9" style="fill:#008000;stroke:#008000;stroke-opacity:1" /></g></g><text x="270.09064" y="66.906364" transform="scale(1.1082192,0.90234857)" id="text7608" xml:space="preserve" style="font-size:43.24214554px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="270.09064" y="66.906364" id="tspan7610">}</tspan></text>
        <text x="270.09064" y="129.21878" transform="scale(1.1082192,0.90234857)" id="text7608-0" xml:space="preserve" style="font-size:43.24214554px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="270.09064" y="129.21878" id="tspan7610-6">}</tspan></text>
        <text x="330.33087" y="60.88369" id="text7633" xml:space="preserve" style="font-size:15.01670647px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="330.33087" y="60.88369" id="tspan7635" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;fill:#0000ff;font-family:Arial;-inkscape-font-specification:Arial">Your code</tspan><tspan x="330.33087" y="79.654572" id="tspan7637" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;fill:#0000ff;font-family:Arial;-inkscape-font-specification:Arial">which does</tspan><tspan x="330.33087" y="98.425453" id="tspan7639" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;fill:#0000ff;font-family:Arial;-inkscape-font-specification:Arial">the actual</tspan><tspan x="330.33087" y="117.19634" id="tspan7641" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;fill:#0000ff;font-family:Arial;-inkscape-font-specification:Arial">work!</tspan></text>
        <text x="6.2617145" y="89.451149" id="text7600" xml:space="preserve" style="font-size:15.01670647px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="6.2617145" y="89.451149" id="tspan7602" style="font-size:12.87146473px;fill:#008000;font-family:arial;-inkscape-font-specification:arial">2. Decorate</tspan><tspan x="6.2617145" y="105.54048" id="tspan7604" style="font-size:12.87146473px;fill:#008000;font-family:arial;-inkscape-font-specification:arial">    pipeline</tspan><tspan x="6.2617145" y="121.62981" id="tspan7606" style="font-size:12.87146473px;fill:#008000;font-family:arial;-inkscape-font-specification:arial">    functions</tspan></text>
        </svg>

    
    The functions which do the actual work of each stage of the pipeline remain unchanged.
    The role of **Ruffus** is to make sure these functions are called in the right order, 
    with the right parameters, running in parallel using multiprocessing if desired.
        
    There are three simple parts to building a **ruffus** pipeline

        #. importing ruffus
        #. "Decorating" functions which are part of the pipeline
        #. Running the pipeline!
    
.. index:: 
    pair: decorators; Tutorial
    

****************************
"Decorators"
****************************

    You need to tag or :term:`decorator` existing code to tell **Ruffus** that they are part
    of the pipeline.
    
    .. note::
        
        python :term:`decorator`\ s are ways to tag or mark out functions. 

        They start with a ``@`` prefix and take a number of parameters in parenthesis.

        .. :: .. image:: ../../images/simple_tutorial_decorator_syntax.png

        .. raw:: html

            <svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0"
            	 width="249.5pt" height="67.5pt" viewBox="0 0 249.5 67.5">
            <g transform="scale(1)">
                <rect x="4.5" y="14.667" fill="#eeffcc" stroke="#016735" stroke-width="0.25" stroke-miterlimit="10" width="157" height="52.833"/>
                <rect x="3.25" y="14.667" fill="#eeffcc" width="159.5" height="52.833"/>
                <text transform="matrix(1 0 0 1 14.5 33.6177)"><tspan x="0" y="0" font-family="'Courier'" font-weight="bold"  font-size="12">@follows</tspan><tspan x="57.609" y="0" font-family="'Courier'" font-size="12">(first_task)</tspan><tspan x="0" y="14.4" fill="#006838" font-family="'Courier'" font-weight="bold"  font-size="12">def</tspan><tspan x="21.604" y="14.4" font-family="'Courier'" font-size="12"> second_task():</tspan><tspan x="0" y="28.8" font-family="'Courier'" font-size="12">    &quot;&quot;</tspan><tspan x="0" y="43.2" font-family="'Courier'" font-size="12" letter-spacing="28">	</tspan></text>
                <path fill="none" stroke="#ED1C24" stroke-miterlimit="10" d="M73.25,29.762c0,4.688-3.731,8.488-8.333,8.488H18.083
                	c-4.602,0-8.333-3.8-8.333-8.488l0,0c0-4.688,3.731-8.488,8.333-8.488h46.834C69.519,21.274,73.25,25.075,73.25,29.762L73.25,29.762
                	z"/>
                <g>
                	<g>
                		<line fill="none" stroke="#FF0000" stroke-miterlimit="10" x1="74.775" y1="20.142" x2="106" y2="7.5"/>
                		<g>
                			<path fill="#ED1C24" d="M71.978,21.274c1.514-0.044,3.484,0.127,4.854,0.6l-1.689-1.881l-0.095-2.526
                				C74.392,18.759,73.097,20.253,71.978,21.274z"/>
                		</g>
                	</g>
                </g>
                <text transform="matrix(1 0 0 1 107.75 11.5)" fill="#FF0000" " font-size="12">Decorator</text>
                <text transform="matrix(1 0 0 1 170.75 50.75)"><tspan x="0" y="0" fill="#0000FF" font-size="12">Normal Python </tspan><tspan x="0" y="14.4" fill="#0000FF" font-size="12">Function</tspan></text>
                <g>
                	<line fill="#0000FF" x1="166.5" y1="46.5" x2="147" y2="46.5"/>
                	<g>
                		<line fill="none" stroke="#0000FF" stroke-miterlimit="10" x1="166.5" y1="46.5" x2="150.018" y2="46.5"/>
                		<g>
                			<path fill="#0000FF" d="M147,46.5c1.42-0.527,3.182-1.426,4.273-2.378l-0.86,2.378l0.86,2.377
                				C150.182,47.925,148.42,47.026,147,46.5z"/>
                		</g>
                	</g>
                </g>
            </g>
            </svg>
                
    The **ruffus** decorator :ref:`@follows <decorators.follows>` makes sure that
    ``second_task`` follows ``first_task``.
    

    | Multiple :term:`decorator`\ s can be used for each :term:`task` function to add functionality
      to *Ruffus* pipeline functions. 
    | However, the decorated python functions can still be
      called normally, outside of *Ruffus*.
    | *Ruffus* :term:`decorator`\ s can be added to (stacked on top of) any function in any order.

    * :ref:`More on @follows in the in the Ruffus `Manual <manual.follows>`
    * :ref:`@follows syntax in detail <decorators.follows>`


.. index:: 
    pair: pipeline_run; Tutorial

****************************
Running the pipeline
****************************

    We run the pipeline by specifying the **last** stage (:term:`task` function) of your pipeline.
    Ruffus will know what other functions this depends on, following the appropriate chain of
    dependencies automatically, making sure that the entire pipeline is up-to-date.

    Because ``second_task`` depends on ``first_task``, both functions are executed in order.

        ::
            
            >>> pipeline_run([second_task], verbose = 1)
        
    Ruffus by default prints out the ``verbose`` progress through the pipelined code, 
    interleaved with the **Hello** printed by ``first_task`` and **World** printed
    by ``second_task``.
    
            
    
        .. ::
            
            >>> pipeline_run([second_task], verbose = 1)
            Start Task = first_task
            Hello
                Job completed
            Completed Task = first_task
            Start Task = second_task
            world
                Job completed
            Completed Task = second_task


        .. raw:: html

            <svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0"
                 width="375pt" height="108pt" viewBox="0 0 375 108">        
            <rect width="359.146" height="95.347786" x="7.8544765" y="6.3284979" id="rect3521" style="fill:none;stroke:#016735;stroke-width:0.18506026;stroke-miterlimit:10" /><rect width="362.35596" height="95.347786" x="6.2499924" y="6.3284979" id="rect3523" style="fill:#eeffcc" />
            <text x="9.2210703" y="18.304934" id="text3345" xml:space="preserve" style="font-size:10.39404392px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="9.2210703" y="18.304934" id="tspan3347"><tspan id="tspan3365" style="font-weight:bold;fill:#ff0000;-inkscape-font-specification:Monospace Bold">&gt;&gt;&gt;</tspan> pipeline_run([second_task], verbose = 1)</tspan><tspan x="9.2210703" y="31.297489" id="tspan3351" style="font-weight:bold;fill:#0000ff">Hello</tspan><tspan x="9.2210703" y="44.449203" id="tspan3353">    Job completed</tspan><tspan x="9.2210703" y="57.441757" id="tspan3355">Completed Task = first_task</tspan><tspan x="9.2210703" y="70.275154" id="tspan3359" style="font-weight:bold;fill:#0000ff">world</tspan><tspan x="9.2210703" y="83.426872" id="tspan3361">    Job completed</tspan><tspan x="9.2210703" y="96.419426" id="tspan3363">Completed Task = second_task</tspan></text>
            <text x="392.0932" y="73.633965" transform="scale(0.78097325,1.2804536)" id="text3373" xml:space="preserve" style="font-size:17.92634964px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Monospace;-inkscape-font-specification:Monospace"><tspan x="392.0932" y="73.633965" id="tspan3375"> </tspan></text>
            </svg>
    
    
    

