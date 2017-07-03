module.exports = {
  entry: [
    './src/index.js'
  ],
  output: {
    path: __dirname,
    publicPath: '/',
    filename: 'app.js'
  },
  module: {
    loaders: [
      {
        test: /\.(js|jsx)$/,
        loaders: ["babel-loader"],
        exclude: [/node_modules/]
      },
      {
        test: /\.css$/,
        loaders: ['style-loader', 'css-loader?modules']
      }
    ]
  },
  devServer: {
    historyApiFallback: true,
    contentBase: './'
  },
  externals: {
    'config': 'Hello'
  }
};
