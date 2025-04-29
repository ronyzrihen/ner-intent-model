# Use AWS Lambda base image for Python 3.8
FROM public.ecr.aws/lambda/python:3.13

RUN pip install --upgrade pip
RUN pip install torch \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    transformers numpy
RUN pip install wordninja

COPY Lambdas/classify.py ./

CMD ["classify.lambda_handler"]