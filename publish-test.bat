rd /s /q  dist
rd /s /q  build
rd /s /q  hytest.egg-info

python -m build --wheel  && twine upload dist/* --repository testpypi

pause