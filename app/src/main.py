from contextlib import redirect_stdout
from io import StringIO



from flask import Flask, request

port = 55001

print("Trying to run a socket server on:", port)


class PythonRunner:
    __globals = {}
    __locals = {}

    def run(self, code):
        f = StringIO()
        with redirect_stdout(f):
            exec(code, self.__globals, self.__locals)
        return f.getvalue()


pr = PythonRunner()


app = Flask(__name__)


@app.route("/")
def hello_world():

    try :
        import traceback
        import sys
        from transformers import TFAutoModelForCausalLM, AutoTokenizer

    except Exception as e:
        return str(traceback.format_exc()) + "\n\n IMPORTING ##########" + "\n\n" + sys.version

    try :
        checkpoint = "assets/qwen"
        model = TFAutoModelForCausalLM.from_pretrained(checkpoint)
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    except Exception as e:
        return str(traceback.format_exc()) + "\n\n LOADING##########################"

    try :

        inputs = tokenizer.encode("Hello  ", return_tensors="tf")

        outputs = model.generate(inputs, max_new_tokens=500, temperature=0.2, top_p=0.9, do_sample=True)

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return generated_text

    except :
        return str(traceback.format_exc()) + "\n\n finsl ##########"



@app.route("/python", methods=["POST"])
def run_python():
    try:
        return pr.run(request.json["command"])
    except Exception as e:
        return str(e)

app.run(port=port)