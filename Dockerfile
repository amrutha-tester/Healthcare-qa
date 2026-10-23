FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

WORKDIR /app

# Install Python test dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-playwright \
    pytest-html \
    pytest-base-url \
    faker \
    python-dotenv \
    pydantic-settings \
    requests && \
    playwright install --with-deps chromium firefox webkit

# Copy test suite and source code into the container
COPY . .

# Create reports directory for JUnit XML, HTML reports, and Playwright traces
RUN mkdir -p /app/reports /app/test-results

# Default command runs pytest in headless mode (overrides --headed in pytest.ini)
CMD ["pytest", "-o", "addopts=-v --browser=chromium --tracing=retain-on-failure --screenshot=only-on-failure", "--junitxml=reports/junit.xml", "--html=reports/report.html", "--self-contained-html"]
