echo Running test_file_name_parameters.py                                           && \
python3 -m unittest test_file_name_parameters                                       && \
echo Running test_with_logger.py                                                    && \
python3 -m unittest test_with_logger                                                && \
echo Running script test_with_logger.py                                             && \
python3 test_with_logger.py                                                         && \
echo Running test_proxy_logger.py                                                   && \
python3 -m unittest test_proxy_logger                                               && \
echo Running test_exceptions.py                                                     && \
python3 -m unittest test_exceptions                                                 && \
echo Running test_task_file_dependencies.py                                         && \
python3 -m unittest test_task_file_dependencies                                     && \
echo Running test_task_misc.py                                                      && \
python3 -m unittest test_task_misc                                                  && \
echo Running test_inputs_with_multiple_args_raising_exception.py                    && \
python3 -m unittest test_inputs_with_multiple_args_raising_exception                && \
echo Running test_collate.py                                                        && \
python3 -m unittest test_collate                                                    && \
echo Running test_empty_files_decorator.py                                          && \
python3 -m unittest test_empty_files_decorator                                      && \
echo Running test_transform_with_no_re_matches.py                                   && \
python3 -m unittest test_transform_with_no_re_matches                               && \
echo Running test_transform_inputs.py                                               && \
python3 -m unittest test_transform_inputs                                           && \
echo Running test_files_decorator.py                                                && \
python3 -m unittest test_files_decorator                                            && \
echo Running test_verbosity.py                                                      && \
python3 -m unittest test_verbosity                                                  && \
echo Running test_transform_add_inputs.py                                           && \
python3 -m unittest test_transform_add_inputs                                       && \
echo Running test_split_regex_and_collate.py                                        && \
python3 -m unittest test_split_regex_and_collate                                    && \
echo Running test_tutorial7.py                                                      && \
python3 -m unittest test_tutorial7                                                  && \
echo Running test_ruffus_utility.py                                                 && \
python3 -m unittest test_ruffus_utility                                             && \
echo Running test_filesre_combine.py                                                && \
python3 -m unittest test_filesre_combine                                            && \
echo Running test_filesre_split_and_combine.py                                      && \
python3 -m unittest test_filesre_split_and_combine                                  && \
echo Running test_branching_dependencies.py                                         && \
python3 -m unittest test_branching_dependencies                                     && \
echo Running test_split_and_combine.py                                              && \
python3 -m unittest test_split_and_combine                                          && \
echo Running test_runtime_data.py                                                   && \
python3 -m unittest test_runtime_data                                               && \
echo Running test_pausing.py                                                        && \
python3 -m unittest test_pausing                                                    && \
echo Running test_active_if.py                                                      && \
python3 -m unittest test_active_if                                                  && \
echo Running test_softlink_uptodate.py                                              && \
python3 -m unittest test_softlink_uptodate                                          && \
echo Running test_newstyle_proxy.py                                                 && \
python3 -m unittest test_newstyle_proxy                                             && \
echo Running test_job_history_with_exceptions.py                                    && \
python3 -m unittest test_job_history_with_exceptions                                && \
echo Running test_mkdir.py                                                          && \
python3 -m unittest test_mkdir                                                      && \
echo Running test_posttask_merge.py                                                 && \
python3 -m unittest test_posttask_merge                                             && \
echo Running test_cmdline.py                                                        && \
python3 -m unittest test_cmdline                                                    && \
echo Running test_graphviz.py                                                       && \
python3 -m unittest test_graphviz                                                   && \
echo Running test_ruffus_utility_parse_task_arguments.py                            && \
python3 -m unittest test_ruffus_utility_parse_task_arguments                        && \
echo Running test_split_subdivide_checkpointing.py                                  && \
python3 -m unittest test_split_subdivide_checkpointing                              && \
echo Running test_pipeline_printout_graph.py                                        && \
python3 -m unittest test_pipeline_printout_graph                                    && \
echo Running test_follows_mkdir.py                                                  && \
python3 -m unittest test_follows_mkdir                                              && \
echo Running test_N_x_M_and_collate.py                                              && \
python3 -m unittest test_N_x_M_and_collate                                          && \
echo Running test_unicode_filenames.py                                              && \
python3 -m unittest test_unicode_filenames                                          && \
echo Running test_subpipeline.py                                                    && \
python3 -m unittest test_subpipeline                                                && \
# fragile tests involving error messages
echo Running test_regex_error_messages.py                                           && \
python3 -m unittest test_regex_error_messages                                       && \
echo Running test_newstyle_regex_error_messages.py                                  && \
python3 -m unittest test_newstyle_regex_error_messages                              && \
echo Running test_combinatorics.py                                                  && \
python3 -m unittest test_combinatorics                                              && \
echo Running test_newstyle_combinatorics.py                                         && \
python3 -m unittest test_newstyle_combinatorics                                     && \
echo Running test_job_completion_checksums.py                                       && \
python3 -m unittest test_job_completion_checksums                                   && \
echo Running test_transform_formatter.py                                            && \
python3 -m unittest test_transform_formatter                                        && \
echo DONE!!!                                                                        

