module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    devtool: 'source-map',
    module: {
      rules: [
        {
          test: /\.(csv|xlsx|xls)$/,
          loader: 'file-loader',
          options: {
            name: `defaults/[name].[ext]`
          }
        }
      ],
     }
  },
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    progress: false,
    watchOptions: {
      aggregateTimeout: 500, 
      poll: 1000,
      ignored: /node_modules/
    }
  }
}
