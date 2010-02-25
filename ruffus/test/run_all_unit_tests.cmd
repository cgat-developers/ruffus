echo Running  ./test_ruffus_utility.py
python ./test_ruffus_utility.py
echo Running  ./test_file_name_parameters.py
python ./test_file_name_parameters.py
echo Running  ./test_filesre_combine.py
python ./test_filesre_combine.py -D
echo Running  ./test_filesre_combine.py
python ./test_filesre_combine.py -D -j 10
echo Running  ./test_filesre_split_and_combine.py
python ./test_filesre_split_and_combine.py -D
echo Running  ./test_filesre_split_and_combine.py
python ./test_filesre_split_and_combine.py -D -j 10
echo Running  ./test_branching_dependencies.py
python ./test_branching_dependencies.py -D
echo Running  ./test_branching_dependencies.py
python ./test_branching_dependencies.py -D -j 10
echo Running  ./test_exceptions.py
python ./test_exceptions.py 
echo Running  ./test_task_file_dependencies.py
python ./test_task_file_dependencies.py 
echo Running  ./test_task_misc.py
python ./test_task_misc.py 
echo Running  ./test_follows_mkdir.py
python ./test_follows_mkdir.py
echo Running  ./test_N_x_M_and_collate.py
python ./test_N_x_M_and_collate.py --debug
echo Running  ./test_collate.py
python ./test_collate.py --debug
echo Running  ./test_split_and_combine.py
python ./test_split_and_combine.py -D -j 10
echo Running  ./simpler_at_runtime.py
python ./simpler_at_runtime.py
echo Running  ./test_unicode_filenames.py
python ./test_unicode_filenames.py
echo Running  ./test_inputs_with_multiple_args_raising_exception.py
python ./test_inputs_with_multiple_args_raising_exception.py
echo Running  ./test_pausing.py
python ./test_pausing.py --debug -j 10
echo Running  ./test_transform_with_no_re_matches.py
python ./test_transform_with_no_re_matches.py
