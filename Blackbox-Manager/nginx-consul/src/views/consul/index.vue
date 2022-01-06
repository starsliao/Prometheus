<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.module" placeholder="监控类型" clearable style="width: 200px" class="filter-item">
        <el-option v-for="item in module_list" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.company" placeholder="公司" clearable style="width: 100px" class="filter-item">
        <el-option v-for="item in company_list" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.project" filterable placeholder="项目" clearable style="width: 160px" class="filter-item">
        <el-option v-for="item in project_list" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.env" filterable placeholder="环境" clearable style="width: 80px" class="filter-item">
        <el-option v-for="item in env_list" :key="item" :label="item" :value="item" />
      </el-select>

      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        新增
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        导出
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="all_list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" align="center" width="60px">
        <template slot-scope="scope">
          <span>{{ scope.$index+1 }}</span>
        </template>
      </el-table-column>
      <el-table-column label="监控类型" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.module }}</span>
        </template>
      </el-table-column>
      <el-table-column label="公司" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.company }}</span>
        </template>
      </el-table-column>
      <el-table-column label="项目" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.project }}</span>
        </template>
      </el-table-column>
      <el-table-column label="环境" align="center" width="60px">
        <template slot-scope="{row}">
          <span>{{ row.env }}</span>
        </template>
      </el-table-column>
      <el-table-column label="名称" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="实例" align="center">
        <template slot-scope="{row}">
          <span style="font-size: 12px">{{ row.instance }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="160" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row,$index)">
            编辑
          </el-button>
          <el-button size="mini" type="danger" @click="handleDelete(row,$index)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="fetchData" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="40%">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="80px" style="width: 400px; margin-left:50px;">
        <el-form-item label="监控类型" prop="module">
          <el-autocomplete v-model="temp.module" :fetch-suggestions="Sugg_module" placeholder="优先选择" clearable style="width: 360px" class="filter-item" />
        </el-form-item>
        <el-form-item label="公司" prop="company">
          <el-autocomplete v-model="temp.company" :fetch-suggestions="Sugg_company" placeholder="优先选择" clearable style="width: 360px" class="filter-item" />
        </el-form-item>
        <el-form-item label="项目" prop="project">
          <el-autocomplete v-model="temp.project" :fetch-suggestions="Sugg_project" placeholder="优先选择" clearable style="width: 360px" class="filter-item" />
        </el-form-item>
        <el-form-item label="环境" prop="env">
          <el-autocomplete v-model="temp.env" :fetch-suggestions="Sugg_env" placeholder="优先选择" clearable style="width: 360px" class="filter-item" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name" placeholder="请输入" clearable style="width: 360px" class="filter-item" />
        </el-form-item>
        <el-form-item label="实例" prop="instance">
          <el-input v-model="temp.instance" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="请输入" style="width: 360px" class="filter-item" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

import { getAllList, getAllInfo, addService, updateService, delService } from '@/api/consul'
export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      new_list: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        module: '',
        company: '',
        project: '',
        env: '',
        sort: '+id'
      },
      value_module: [],
      value_company: [],
      value_project: [],
      value_env: [],
      importanceOptions: [1, 2, 3],
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      up_index: 0,
      del_dict: {},
      temp: {
        module: '',
        company: '',
        project: '',
        env: '',
        name: '',
        instance: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '更新',
        create: '创建'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        module: [{ required: true, message: '此为必填项', trigger: 'change' }],
        company: [{ required: true, message: '此为必填项', trigger: 'change' }],
        project: [{ required: true, message: '此为必填项', trigger: 'change' }],
        env: [{ required: true, message: '此为必填项', trigger: 'change' }],
        name: [{ required: true, message: '此为必填项', trigger: 'change' }],
        instance: [{ required: true, message: '此为必填项', trigger: 'change' }]
      },
      downloadLoading: false
    }
  },

  computed: {
    cmodule() {
      return this.listQuery.module
    },
    ccompany() {
      return this.listQuery.company
    },
    cproject() {
      return this.listQuery.project
    },
    cenv() {
      return this.listQuery.env
    }
  },

  watch: {
    cmodule(new_module) {
      this.fetchList(new_module, this.listQuery.company, this.listQuery.project, this.listQuery.env)
    },
    ccompany(new_company) {
      this.fetchList(this.listQuery.module, new_company, this.listQuery.project, this.listQuery.env)
    },
    cproject(new_project) {
      this.fetchList(this.listQuery.module, this.listQuery.company, new_project, this.listQuery.env)
    },
    cenv(new_env) {
      this.fetchList(this.listQuery.module, this.listQuery.company, this.listQuery.project, new_env)
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      this.listLoading = true
      getAllInfo().then(response => {
        this.all_list = response.all_list
        this.module_list = response.module_list
        this.company_list = response.company_list
        this.project_list = response.project_list
        this.env_list = response.env_list
        this.listLoading = false
        this.xmodule = this.load_module()
        this.xcompany = this.load_company()
        this.xproject = this.load_project()
        this.xenv = this.load_env()
      })
    },
    fetchList(module, company, project, env) {
      this.listLoading = true
      getAllList(module, company, project, env).then(response => {
        this.all_list = response.all_list
        this.listLoading = false
        this.module_list = response.module_list
        this.company_list = response.company_list
        this.project_list = response.project_list
        this.env_list = response.env_list
      })
    },

    handleFilter() {
      this.listQuery.page = 1
      this.fetchData()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作Success',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        status: 'published',
        type: ''
      }
    },

    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          addService(this.temp).then(response => {
            this.all_list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$message({
              message: response.data,
              type: 'success'
            })
          })
        }
      })
    },
    handleUpdate(row, index) {
      this.temp = Object.assign({}, row) // copy obj
      this.del_dict = Object.assign({}, row)
      this.up_index = index
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const up_dict = Object.assign({}, this.temp)
          updateService(this.del_dict, up_dict).then(response => {
            this.all_list.splice(this.up_index, 1, this.temp)
            this.dialogFormVisible = false
            this.$message({
              message: response.data,
              type: 'success'
            })
          })
        }
      })
    },
    handleDelete(row, index) {
      this.$confirm('此操作将删除【' + row.env + '：' + row.project + '：' + row.name + '】，是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delService(row).then(response => {
          this.$message({
            message: response.data,
            type: 'success'
          })
          this.all_list.splice(index, 1)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },

    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'module', 'company', 'project', 'env', 'name', 'instance']
        const filterVal = ['timestamp', 'module', 'company', 'project', 'env', 'name', 'instance']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.all_list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    Sugg_module(queryString, cb) {
      var xmodule = this.xmodule
      var results = queryString ? xmodule.filter(this.createFilter(queryString)) : xmodule
      cb(results)
    },
    Sugg_company(queryString, cb) {
      var xcompany = this.xcompany
      var results = queryString ? xcompany.filter(this.createFilter(queryString)) : xcompany
      cb(results)
    },
    Sugg_project(queryString, cb) {
      var xproject = this.xproject
      var results = queryString ? xproject.filter(this.createFilter(queryString)) : xproject
      cb(results)
    },
    Sugg_env(queryString, cb) {
      var xenv = this.xenv
      var results = queryString ? xenv.filter(this.createFilter(queryString)) : xenv
      cb(results)
    },
    createFilter(queryString) {
      return (restaurant) => {
        return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },
    load_module() {
      for (const x in this.module_list) {
        this.value_module.push({ 'value': this.module_list[x] })
      }
      return this.value_module
    },
    load_company() {
      for (const x in this.company_list) {
        this.value_company.push({ 'value': this.company_list[x] })
      }
      return this.value_company
    },
    load_project() {
      for (const x in this.project_list) {
        this.value_project.push({ 'value': this.project_list[x] })
      }
      return this.value_project
    },
    load_env() {
      for (const x in this.env_list) {
        this.value_env.push({ 'value': this.env_list[x] })
      }
      return this.value_env
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
