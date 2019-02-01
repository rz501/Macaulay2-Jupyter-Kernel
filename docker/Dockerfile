FROM jupyter/base-notebook

# install m2jk and copy examples
RUN python3 -m pip install macaulay2-jupyter-kernel
RUN python3 -m m2_kernel.install
COPY test.ipynb /test/
COPY demo.ipynb /test/

# install M2
USER root
RUN apt-get update && apt-get install -y gnupg2
RUN echo 'deb https://faculty.math.illinois.edu/Macaulay2/Repositories/Ubuntu bionic main' >/etc/apt/sources.list.d/macaulay2.list
RUN wget http://www.math.uiuc.edu/Macaulay2/PublicKeys/Macaulay2-key
RUN apt-key add Macaulay2-key
RUN apt-get update && apt-get install -y macaulay2

# run jupyter notebook
USER jovyan
WORKDIR /test
ENTRYPOINT ["jupyter", "notebook", "--port", "8890", "--no-browser"]
EXPOSE 8890