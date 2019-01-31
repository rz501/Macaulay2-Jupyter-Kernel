FROM unlhcc/macaulay2
RUN useradd -ms /bin/bash tester
WORKDIR /home/tester
COPY *.py /home/tester/
COPY *.ipynb /home/tester/
USER root
RUN python3 get-pip.py
RUN pip3 install jupyter
# RUN pip3 install notebook==5.6.0
# RUN python3 -m pip install jupyter
# RUN chown tester /home/tester/.local
RUN chmod -R 0777 /home/tester
USER tester
# ENTRYPOINT ["jupyter", "notebook", "--port", "8895", "--no-browser"]
ENTRYPOINT ["jupyter", "notebook", "--ip=127.0.0.1", "--port", "8895", "--no-browser"]
# ENTRYPOINT ["jupyter", "notebook", "--ip=127.0.0.1", "--no-browser"]
EXPOSE 8895