FROM taktile/base-serving-api:3823753de9664890706d4baeb76f8b7807c6c213
ENV APPDIR /app

# Install requirements
COPY ./requirements.txt ${APPDIR}/user_requirements.txt
RUN pip install -r ${APPDIR}/user_requirements.txt

# Copy code and assets for running the application
COPY ./src ${APPDIR}/src
COPY ./assets ${APPDIR}/assets
COPY ./tests ${APPDIR}/user_tests

# Run model profile
RUN python ${APPDIR}/profile_endpoints.py
