import js2py

result, tempfile = js2py.run_file("step2.js")
result= tempfile.sayHello("risa")
print(result)
