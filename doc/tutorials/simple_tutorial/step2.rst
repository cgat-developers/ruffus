.. include:: ../../global.inc
.. _Simple_Tutorial_2nd_step:

.. index::
    pair: @transform; Tutorial

###################################################################
Step 2: Passing parameters to the pipeline
###################################################################

   * :ref:`Simple tutorial overview <Simple_Tutorial>`
   * :ref:`@transform syntax in detail <decorators.transform>`

.. note::

    Remember to look at the example code:

    * :ref:`Python Code for step 2 <Simple_Tutorial_2nd_step_code>`

***************************************
Overview
***************************************
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


    Computational pipelines transform your data in stages until the final result is produced.
    Ruffus automates the plumbing in your pipeline. You supply the python functions which perform the data transformation,
    and tell Ruffus how these pipeline stages or :term:`task` functions are connected together.

    .. note::

        **The best way to design a pipeline is to:**

            * **write down the file names of the data as it flows across your pipeline**
            * **write down the names of functions which transforms the data at each stage of the pipeline.**


    By letting **Ruffus** manage your pipeline parameters, you will get the following features
    for free:

        #. only out-of-date parts of the pipeline will be re-run
        #. multiple jobs can be run in parallel (on different processors if possible)
        #. pipeline stages can be chained together automatically




************************************
@transform
************************************
    Let us start with the simplest pipeline with a single *input* data file **transform**\ed
    into a single *output* file. We will add some arbitrary extra parameters as well.

    The :ref:`@transform <decorators.transform>` decorator tells Ruffus that this
    task function **transforms** each and every piece of input data into a corresponding output.

        In other words, inputs and outputs have a **1 to 1** relationship.

    .. note::

        In the second part of the tutorial, we will encounter more decorators which can *split up*, or *join together* or *group* inputs.

            In other words, inputs and output can have **many to one**, **many to many** etc. relationships.



    Let us provide **input**\s and **output**\s to our new pipeline:

        .. raw:: html

            <svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0"
                width="385pt"
                height="210pt"
                viewBox="0 0 385 210">
                    <defs id="defs3568">
                <marker refX="0" refY="0" orient="auto" id="Arrow2Mend" style="overflow:visible">
                  <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="scale(-0.6,-0.6)" id="path4497" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
                </marker>
                <marker refX="0" refY="0" orient="auto" id="Arrow1Lend" style="overflow:visible">
                  <path d="M 0,0 5,-5 -12.5,0 5,5 0,0 z" transform="matrix(-0.8,0,0,-0.8,-10,0)" id="path4473" style="fill-rule:evenodd;stroke:#000000;stroke-width:1pt" />
                </marker>
                <marker refX="0" refY="0" orient="auto" id="TriangleOutL" style="overflow:visible">
                  <path d="m 5.77,0 -8.65,5 0,-10 8.65,5 z" transform="scale(0.8,0.8)" id="path4612" style="fill-rule:evenodd;stroke:#000000;stroke-width:1pt" />
                </marker>
                <marker refX="0" refY="0" orient="auto" id="Arrow2Send" style="overflow:visible">
                  <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="matrix(-0.3,0,0,-0.3,0.69,0)" id="path4503" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
                </marker>
                <marker refX="0" refY="0" orient="auto" id="Arrow1Mend" style="overflow:visible">
                  <path d="M 0,0 5,-5 -12.5,0 5,5 0,0 z" transform="matrix(-0.4,0,0,-0.4,-4,0)" id="path4479" style="fill-rule:evenodd;stroke:#000000;stroke-width:1pt" />
                </marker>
                <marker refX="0" refY="0" orient="auto" id="Arrow2Lend" style="overflow:visible">
                  <path d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z" transform="matrix(-1.1,0,0,-1.1,-1.1,0)" id="path4491" style="fill-rule:evenodd;stroke-width:0.625;stroke-linejoin:round" />
                </marker>
              </defs>
              <g transform="matrix(1.0077068,0,0,1,9.8598546,3.6099157)" id="g3519">
                <rect width="359.146" height="174.006" x="6.244" y="27.667" id="rect3521" style="fill:none;stroke:#016735;stroke-width:0.25;stroke-miterlimit:10" />
                <rect width="364.86499" height="174.006" x="3.385" y="27.667" id="rect3523" style="fill:#eeffcc" />
              </g>
              <path d="m 84.221497,82.954914 c 0,3.583 -3.942,6.488 -8.804,6.488 h -49.481 c -4.862,0 -8.803999,-2.905 -8.803999,-6.488 l 0,0 c 0,-3.582998 3.941999,-6.487998 8.803999,-6.487998 h 49.481 c 4.862,0 8.804,2.905 8.804,6.487998 l 0,0 z" id="path3641" style="opacity:0.2;fill:#ed1c24" />
              <path d="m 190.77333,82.954914 c 0,3.583 -6.09517,6.488 -13.61411,6.488 h -76.51461 c -7.518948,0 -13.614113,-2.905 -13.614113,-6.488 l 0,0 c 0,-3.582998 6.095165,-6.487998 13.614113,-6.487998 h 76.51322 c 7.51894,0 13.6155,2.905 13.6155,6.487998 l 0,0 z" id="path3671" style="opacity:0.2;fill:#00a14b" />
              <path d="m 368.12884,82.954914 c 0,3.583 -3.66127,6.488 -8.17701,6.488 h -45.95795 c -4.5166,0 -8.17787,-2.905 -8.17787,-6.488 l 0,0 c 0,-3.582998 3.66127,-6.487998 8.17787,-6.487998 h 45.95795 c 4.51574,0 8.17701,2.905 8.17701,6.487998 l 0,0 z" id="path3687" style="opacity:0.2;fill:#00a14b" />
              <path d="m 300.38251,97.842914 c 0,3.406006 -2.537,6.167006 -5.667,6.167006 H 90.049497 c -3.129,0 -5.667,-2.761 -5.667,-6.167006 l 0,0 c 0,-3.406 2.537,-6.167 5.667,-6.167 H 294.71651 c 3.129,10e-4 5.666,2.762 5.666,6.167 l 0,0 z" id="path3689" style="opacity:0.2;fill:#00a14b" />
              <text x="22.156881" y="58.294636" transform="scale(1.0042467,0.99577126)" id="text3295" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace" />
              <text x="22.156881" y="138.88107" transform="scale(1.0042467,0.99577126)" id="text3317" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace" />
              <text x="22.156881" y="179.17427" transform="scale(1.0042467,0.99577126)" id="text3327" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace" />
              <text x="22.156881" y="206.03641" transform="scale(1.0042467,0.99577126)" id="text3331" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace" />
              <text x="22.156881" y="54.504337" transform="scale(1.0042467,0.99577126)" id="text3285-5" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace" />
              <g transform="matrix(1,0,0,1.442061,16.381543,-1.5326283)" id="g3645">
                <line x1="125.896" y1="53.333" x2="125.896" y2="15.667" id="line3647" style="fill:#00ff00" />
                <g id="g3649">
                  <line stroke-miterlimit="10" x1="125.896" y1="49.028" x2="125.896" y2="15.667" id="line3651" style="fill:none;stroke:#00a651;stroke-miterlimit:10" />
                  <g id="g3653">
                    <polygon points="128.888,48.153 125.897,53.333 122.905,48.153 " id="polygon3655" style="fill:#00a651" />
                  </g>
                </g>
              </g>
              <g transform="matrix(1,0,0,1.3096241,27.941781,-1.0861523)" id="g3659">
                <line x1="267.23001" y1="70.667" x2="267.23001" y2="15.667" id="line3661" style="fill:#00ff00" />
                <g id="g3663">
                  <line stroke-miterlimit="10" x1="267.23001" y1="66.361" x2="267.23001" y2="15.667" id="line3665" style="fill:none;stroke:#00a651;stroke-miterlimit:10" />
                  <g id="g3667">
                    <polygon points="270.222,65.486 267.23,70.667 264.238,65.486 " id="polygon3669" style="fill:#00a651" />
                  </g>
                </g>
              </g>
              <g transform="matrix(1,0,0,1.4502473,19.50593,-3.2189853)" id="g3675">
                <line x1="313.56299" y1="53.333" x2="313.56299" y2="15.667" id="line3677" style="fill:#00ff00" />
                <g id="g3679">
                  <line stroke-miterlimit="10" x1="313.56299" y1="49.028" x2="313.56299" y2="15.667" id="line3681" style="fill:none;stroke:#00a651;stroke-miterlimit:10" />
                  <g id="g3683">
                    <polygon points="316.556,48.153 313.564,53.333 310.572,48.153 " id="polygon3685" style="fill:#00a651" />
                  </g>
                </g>
              </g>
              <text x="4.0742145" y="13.589844" id="text3629" style="font-size:12px;fill:#ff0000;font-family:ArialMT">Decorator</text>
              <text x="114.1965" y="15.776917" id="text3643" style="font-size:12px;fill:#00a14b;font-family:ArialMT">Inputs</text>
              <text x="207.08836" y="15.776917" id="text3657" style="font-size:12px;fill:#00a14b;font-family:ArialMT">Extra parameters</text>
              <text x="313.42374" y="15.776917" id="text3673" style="font-size:12px;fill:#00a14b;font-family:ArialMT">Outputs</text>
              <text x="22.156881" y="44.86356" transform="scale(1.0042467,0.99577126)" id="text3285" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace"><tspan id="tspan3287" style="font-weight:bold;fill:#008000">from</tspan> <tspan id="tspan3289" style="font-weight:bold;fill:#0e84b5">ruffus</tspan> <tspan id="tspan3291" style="font-weight:bold;fill:#008000">import</tspan> <tspan id="tspan3293" style="fill:#303030">*</tspan></text>
              <text x="22.156881" y="64.113289" transform="scale(1.0042467,0.99577126)" id="text3329-1" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace">first_task_params = 'job1.input'</text>
              <text x="22.156881" y="86.186874" transform="scale(1.0042467,0.99577126)" id="text3297" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace"><tspan id="tspan3299" style="font-weight:bold;fill:#505050">@transform</tspan>(first_task_params, <tspan id="tspan3548" style="font-weight:bold;fill:#ff0000">suffix</tspan>(&quot;.input&quot;), &quot;.output1&quot;, </text>
              <text x="22.156881" y="99.61795" transform="scale(1.0042467,0.99577126)" id="text3301" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace">           &quot;some_extra.string.for_example&quot;, <tspan id="tspan3303" style="font-weight:bold;fill:#0000d0">14</tspan>)</text>
              <text x="22.156881" y="113.04904" transform="scale(1.0042467,0.99577126)" id="text3305" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace"><tspan id="tspan3307" style="font-weight:bold;fill:#008000">def</tspan> <tspan id="tspan3309" style="font-weight:bold;fill:#0060b0">first_task</tspan>(input_file, output_file,</text>
              <text x="22.156881" y="126.48013" transform="scale(1.0042467,0.99577126)" id="text3311" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace">               extra_parameter_str, extra_parameter_num):</text>
              <text x="22.156881" y="139.91115" transform="scale(1.0042467,0.99577126)" id="text3313" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace">    <tspan id="tspan3315" style="font-weight:bold;fill:#008000">pass</tspan></text>
              <text x="22.156881" y="166.77328" transform="scale(1.0042467,0.99577126)" id="text3319" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace"><tspan id="tspan3321" style="fill:#808080">#   make sure the input file is there</tspan></text>
              <text x="22.156881" y="180.20436" transform="scale(1.0042467,0.99577126)" id="text3323" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace"><tspan id="tspan3325" style="fill:#007020">open</tspan>('job1.input', &quot;w&quot;)</text>
              <text x="22.156881" y="199.1844" transform="scale(1.0042467,0.99577126)" id="text3329" xml:space="preserve" style="font-size:9.89657974px;font-family:monospace">pipeline_run([first_task])</text>
              <path d="m 11.798134,17.75418 0,40.879392 11.506636,16.489166" id="path3696" style="fill:none;stroke:#ff0000;stroke-width:1.25536001;stroke-linecap:butt;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;marker-end:url(#Arrow2Mend)" />
            </svg>


        The ``@transform`` decorator tells Ruffus to generate the appropriate arguments for our python function:

            * The input file name is as given: ``job1.input``
            * The output file name is the input file name with its **suffix** of ``.input`` replaced with ``.output1``
            * There are two extra parameters, a string and a number.

        This is exactly equivalent to the following function call:

            ::

                first_task('job1.input', 'job1.output1', "some_extra.string.for_example", 14)


        Even though this (empty) function doesn't do anything just yet, the output from **Ruffus** ``pipeline_run`` will show that that this part of the pipeline completed successfully:

            .. raw:: html

                <svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="374.86499pt" height="92.02504pt" viewBox="0 0 374.86498 92.025041">
                    <rect width="359.146" height="58.154449" x="7.8589935" y="28.798326" id="rect3521" style="fill:none;stroke:#016735;stroke-width:0.14452712;stroke-miterlimit:10" /><rect width="364.86499" height="58.154449" x="4.9999938" y="28.798326" id="rect3523" style="fill:#eeffcc" />
                    <g transform="matrix(1,0,0,0.72872639,-16.352384,4.6212592)" id="g3645">
                        <line x1="125.896" y1="53.333" x2="125.896" y2="15.667" id="line3647" style="fill:#00ff00" />
                        <g id="g3649">
                            <line stroke-miterlimit="10" x1="125.896" y1="49.028" x2="125.896" y2="15.667" id="line3651" style="fill:none;stroke:#00a651;stroke-miterlimit:10" />
                            <g id="g3653">
                                <polygon points="128.888,48.153 125.897,53.333 122.905,48.153 " id="polygon3655" style="fill:#00a651" />
                            </g>
                        </g>
                    </g>
                    <g transform="matrix(1,0,0,0.73146564,-0.38500643,4.5843285)" id="g3659">
                        <line x1="267.23001" y1="70.667" x2="267.23001" y2="15.667" id="line3661" style="fill:#00ff00" />
                        <g id="g3663">
                            <line stroke-miterlimit="10" x1="267.23001" y1="66.361" x2="267.23001" y2="15.667" id="line3665" style="fill:none;stroke:#00a651;stroke-miterlimit:10" />
                            <g id="g3667">
                                <polygon points="267.23,70.667 264.238,65.486 270.222,65.486 " id="polygon3669" style="fill:#00a651" />
                            </g>
                        </g>
                    </g>
                    <path d="m 153.04485,51.262472 c 0,3.583 -4.15868,6.488 -9.28879,6.488 H 91.550787 c -5.130114,0 -9.288794,-2.905 -9.288794,-6.488 l 0,0 c 0,-3.583 4.15868,-6.488 9.288794,-6.488 h 52.204323 c 5.13012,0 9.28974,2.905 9.28974,6.488 l 0,0 z" id="path3671" style="opacity:0.2;fill:#00a14b" />
                    <g transform="matrix(1,0,0,0.72872639,-103.64072,4.6212592)" id="g3675">
                        <line x1="313.56299" y1="53.333" x2="313.56299" y2="15.667" id="line3677" style="fill:#00ff00" />
                        <g id="g3679">
                            <line stroke-miterlimit="10" x1="313.56299" y1="49.028" x2="313.56299" y2="15.667" id="line3681" style="fill:none;stroke:#00a651;stroke-miterlimit:10" />
                            <g id="g3683">
                                <polygon points="316.556,48.153 313.564,53.333 310.572,48.153 " id="polygon3685" style="fill:#00a651" />
                            </g>
                        </g>
                    </g>
                    <path d="m 250.58388,51.262472 c 0,3.583 -4.83746,6.488 -10.80388,6.488 h -60.72201 c -5.96757,0 -10.80503,-2.905 -10.80503,-6.488 l 0,0 c 0,-3.583 4.83746,-6.488 10.80503,-6.488 H 239.78 c 5.96642,0 10.80388,2.905 10.80388,6.488 l 0,0 z" id="path3687" style="opacity:0.2;fill:#00a14b" />
                    <path d="m 295.61399,65.440811 c 0,3.406 -2.537,6.167 -5.667,6.167 H 85.280993 c -3.129,0 -5.667,-2.761 -5.667,-6.167 l 0,0 c 0,-3.406 2.537,-6.167 5.667,-6.167 H 289.94799 c 3.129,10e-4 5.666,2.762 5.666,6.167 l 0,0 z" id="path3689" style="opacity:0.2;fill:#00a14b" />
                    <text x="92.396126" y="13.742188" id="text3643" style="font-size:12px;fill:#00a14b;font-family:ArialMT">Inputs</text>
                    <text x="193.83928" y="13.742188" id="text3673" style="font-size:12px;fill:#00a14b;font-family:ArialMT">Outputs</text>
                    <text x="256.93237" y="13.742188" id="text3657" style="font-size:12px;fill:#00a14b;font-family:ArialMT">Extra parameters</text>
                    <text x="9.3237839" y="40.037392" id="text3040" xml:space="preserve" style="font-size:10.32079887px;font-family:monospace"><tspan id="tspan3042" style="font-weight:bold;fill:#ff0000">&gt;&gt;&gt;</tspan> pipeline_run([first_task])</text>
                    <text x="9.3237839" y="54.044189" id="text3046" xml:space="preserve" style="font-size:10.32079887px;font-family:monospace">    Job  <tspan id="tspan3048" style="fill:#666666">=</tspan> [job1<tspan id="tspan3050" style="fill:#666666">.</tspan>input <tspan id="tspan3052" style="fill:#666666">-&gt;</tspan> job1<tspan id="tspan3056" style="fill:#666666">.</tspan>output1,</text>
                    <text x="58.633194" y="67.193367" id="text3160" xml:space="preserve" style="font-size:10.32079887px;font-family:monospace">    some_extra.string.for_example, 14] completed</text>
                    <text x="9.3237839" y="82.432899" id="text3058" xml:space="preserve" style="font-size:10.32079887px;font-family:monospace">Completed Task <tspan id="tspan3060" style="fill:#666666">=</tspan> first_task</text>
                    </svg>



************************************
Task functions as recipes
************************************
    This may seem like a lot of effort and complication for something so simple: a normal python function call.
    However, now that we have annotated a task, we can start using it as part of our computational pipeline:


    Each :term:`task` function of the pipeline is a recipe or
    `rule <http://www.gnu.org/software/make/manual/make.html#Rule-Introduction>`_
    which can be applied repeatedly to our data.

    For example, one can have

        * a ``compile()`` *task* which will compile any number of source code files, or
        * a ``count_lines()`` *task* which will count the number of lines in any file or
        * an ``align_dna()`` *task* which will align the DNA of many chromosomes.

    .. note ::

        **Key Ruffus Terminology**:

        A  :term:`task` is an annotated python function which represents a recipe or stage of your pipeline.

        A  :term:`job` is each time your recipe is applied to a piece of data, i.e. each time Ruffus calls your function.

        Each **task** or pipeline recipe can thus have many **jobs** each of which can work in parallel on different data.

    In the original example, we have made a single output file by supplying a single input parameter.
    We shall use much the same syntax to apply the same recipe to *multiple* input files.
    Instead of providing a single *input*, and a single *output*, we are going to specify
    the parameters for *three* jobs at once:

        ::

            # previously,
            # first_task_params = 'job1.input'
            first_task_params = [
                                'job1.input',
                                'job2.input'
                                'job3.input'
                                ]

            # make sure the input files are there
            open('job1.input', "w")
            open('job2.input', "w")
            open('job3.input', "w")

            pipeline_run([first_task])


    .. :: .. image:: ../../images/simple_tutorial_files3.png



    Just by changing the inputs from a single file to a list of three files, we now have a pipeline which runs independently on three pieces of data.
    The results should look familiar:

        ::

            >>> pipeline_run([first_task])
                Job  = [job1.input -> job1.output1,
                        some_extra.string.for_example, 14] completed
                Job  = [job2.input -> job2.output1,
                        some_extra.string.for_example, 14] completed
                Job  = [job3.input -> job3.output1,
                        some_extra.string.for_example, 14] completed
            Completed Task = first_task


************************************
Multiple steps
************************************

    Best of all, it is easy to add another step to our initial pipeline.

    We have to

        * add another ``@transform`` decorated function (``second_task()``),
        * specify ``first_task()`` as the source:
        * use a ``suffix`` which matches the output from ``first_task()``


        ::

            @transform(first_task, suffix(".output1"), ".output2")
            def second_task(input_file, output_file):
                # make output file
                open(output_file, "w")

        * call ``pipeline_run()`` with the correct final task (``second_task()``)


    The full source code can be found :ref:`here <Simple_Tutorial_2nd_step_code>`

    With very little effort, we now have three independent pieces of information coursing through our pipeline.
    Because ``second_task()`` *transforms* the output from ``first_task()``, it magically knows its dependencies and
    that it too has to work on three jobs.


************************************
Multi-tasking
************************************

    Though, three jobs have been specified in parallel, **Ruffus** defaults to running
    each of them successively. With modern CPUs, it is often a lot faster to run parts
    of your pipeline in parallel, all at the same time.

    To do this, all you have to do is to add a multiprocess parameter to pipeline_run:

        ::

            >>> pipeline_run([second_task], multiprocess = 5)

    In this case, ruffus will try to run up to 5 jobs at the same time. Since our second
    task only has three jobs, these will be started simultaneously.



**************************************************
Up-to-date jobs are not re-run unnecessarily
**************************************************

    A job will be run only if the output file timestamps are out of date.
    If you ran the same code a second time,

        ::

            >>> pipeline_run([second_task])


    Nothing would happen because:
        * ``job1.output2`` is more recent than ``job1.output1`` and
        * ``job2.output2`` is more recent than ``job2.output1`` and
        * ``job3.output2`` is more recent than ``job3.output1``.

    Let us see what happens when just 1 out of 3 pieces of data is modified
        ::

            open("job1.input1", "w")
            pipeline_run([second_task], verbose =2, multiprocess = 5)


    You would see that only the out of date jobs (highlighted) have been re-run:

        .. code-block:: pycon
           :emphasize-lines: 2,6

           >>> pipeline_run([second_task], verbose =2, multiprocess = 5)
               Job  = [job1.input -> job1.output1, some_extra.string.for_example, 14] completed
               Job  = [job3.input -> job3.output1, some_extra.string.for_example, 14] unnecessary: already up to date
               Job  = [job2.input -> job2.output1, some_extra.string.for_example, 14] unnecessary: already up to date
           Completed Task = first_task
               Job  = [job1.output1 -> job1.output2] completed
               Job  = [job2.output1 -> job2.output2] unnecessary: already up to date
               Job  = [job3.output1 -> job3.output2] unnecessary: already up to date
           Completed Task = second_task


.. index::
    pair: input / output parameters; Tutorial

***************************************
Intermediate files
***************************************

    In the above examples, the *input* and *output* parameters are file names.
    Ruffus was designed for pipelines which save intermediate data in files. This is not
    compulsory but saving your data in files at each step provides a few advantages:

        #) Ruffus can use file system time stamps to check if your pipeline is up to date
        #) Your data is persistent across runs
        #) This is a good way to pass large amounts of data across processes and computational nodes

    Otherwise, task parameters could be all sorts of data, from lists of files, to numbers,
    sets or tuples. Ruffus imposes few constraints on what *you*
    would like to send to each stage of your pipeline.

    **Ruffus** does, however, assume that all strings in your *input* and *output*
    parameters represent file names.

    *input* parameters which contains a |glob|_ pattern (e.g. ``*.txt``) are expanded to the matching file names.


***************************************
@transform is a 1 to 1 operation
***************************************


    ``@transform`` is a 1:1 operation because it keeps the number of jobs constant
    entering and leaving the task. Each job can accept, for example, a pair of files as its input,
    or generate more than one output files.

    Let us see this in action using the previous example:
        * ``first_task_params`` is changed to 3 *pairs* of file names
        * ``@transform`` for ``first_task`` is modified to produce *pairs* of file names
            * ``.output.1``
            * ``.output.extra.1``


        ::

            from ruffus import *

            #---------------------------------------------------------------
            #   Create pairs of input files
            #
            first_task_params = [
                                 ['job1.a.input', 'job1.b.input'],
                                 ['job2.a.input', 'job2.b.input'],
                                 ['job3.a.input', 'job3.b.input'],
                                ]

            for input_file_pairs in first_task_params:
                for input_file in input_file_pairs:
                    open(input_file, "w")


            #---------------------------------------------------------------
            #
            #   first task
            #
            @transform(first_task_params, suffix(".input"),
                                    [".output.1",
                                     ".output.extra.1"],
                                   "some_extra.string.for_example", 14)
            def first_task(input_files, output_file_pairs,
                            extra_parameter_str, extra_parameter_num):
                # make both pairs of output files
                for output_file in output_file_pairs:
                    open(output_file, "w")


            #---------------------------------------------------------------
            #
            #   second task
            #
            @transform(first_task, suffix(".output.1"), ".output2")
            def second_task(input_files, output_file):
                # make output file
                open(output_file, "w")

            #---------------------------------------------------------------
            #
            #       Run
            #
            pipeline_run([second_task])

        This gives the following results:

        ::

            >>> pipeline_run([pipeline_task])


        We see that apart from having a file pair where previously there was a single file,
        little else has changed. We still have three pieces of data going through the
        pipeline in three parallel jobs.
