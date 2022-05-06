<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default  {
  name:  'App',
    metaInfo() {
        return {
            title: this.$store.state.settings.dynamicTitle && this.$store.state.settings.title,
            titleTemplate: title => {
                return title ? `${title} - ${process.env.VUE_APP_TITLE}` : process.env.VUE_APP_TITLE
            }
        }
    }
}
</script>

<style>
  .el-pagination.is-background {
    text-align: center;
  }
  .pagination-container .el-pagination {
    position: unset;
  }

  #app .sidebar-container .svg-icon {
    /*margin-left: 10px;*/
    font-size: 20px;
  }
</style>
