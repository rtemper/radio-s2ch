#!/bin/bash
cd /app && npm install
/app/node_modules/webpack/bin/webpack.js

echo "build complete"
cp /app/app.js /static/
cp /app/index.html /static/
