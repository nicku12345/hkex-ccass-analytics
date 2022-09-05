FROM node:16

WORKDIR /app

ENV PATH /app/node_modules/.bin$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

COPY . ./
RUN REACT_APP_NODE_ENV=production \
    npm run build
RUN npm install -g serve
CMD serve -s build
