#!/bin/bash

flask db create
flask user create 'kevin_wilson@brown.edu' -l -p asdf
flask run --host 0.0.0.0
