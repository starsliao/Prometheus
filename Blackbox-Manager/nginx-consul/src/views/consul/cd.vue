<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.ver" placeholder="迭代" clearable style="width: 84px" class="filter-item">
        <el-option v-for="item in verlist" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.env" placeholder="请选择部署环境" clearable style="width: 200px" class="filter-item">
        <el-option v-for="(value,key) in envdict" :key="key" :label="value" :value="key" />
      </el-select>
      <el-select v-model="listQuery.namespace" filterable placeholder="命名空间" clearable style="width: 110px" class="filter-item">
        <el-option v-for="item in nslist" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.dpm" filterable placeholder="请选择微服务" clearable style="width: 200px" class="filter-item">
        <el-option v-for="item in nsmslist" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.tag" filterable placeholder="请选择镜像标签" clearable style="width: 180px" class="filter-item">
        <el-option v-for="item in nsmstaglist" :key="item" :label="item.split('：')[1]" :value="item">
          <span style="float: left">{{ item.split('：')[1] }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">{{ item.split('：')[0] }}</span>
        </el-option>
      </el-select>
      <el-select v-model="listQuery.batch" placeholder="批次" clearable style="width: 80px" class="filter-item">
        <el-option v-for="item in batchlist" :key="item" :label="item" :value="item" />
      </el-select>
      <el-checkbox-button v-for="res in reslist" :key="res" v-model="listQuery.resGroup" :label="res" :disabled="res === 'pdb'">{{ res }}</el-checkbox-button>
      <el-button type="success" round icon="el-icon-circle-plus" style="margin-left: 2px;" @click="addms(listQuery)">增加</el-button>
      <el-button :disabled="fresh" type="warning" icon="el-icon-refresh" style="margin-left: 2px;" title="刷新状态(10s)" circle @click="freshlist()" />
    </div>

    <el-table ref="dragTable" v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%">
      <el-table-column width="40px" align="center" label="ID">
        <template slot-scope="scope">
          <span>{{ scope.$index+1 }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="ver" align="center" label="迭代" />
      <el-table-column width="68px" prop="env" align="center" label="环境" />
      <el-table-column width="90px" prop="namespace" align="center" label="命名空间" />
      <el-table-column width="50px" prop="batch" align="center" label="批次" />
      <el-table-column width="200px" prop="microservice" align="center" label="微服务" />

      <el-table-column width="160px" label="标签">
        <template slot-scope="{row}">
          <span>{{ row.tag }}</span>
        </template>
      </el-table-column>

      <el-table-column min-width="220px" label="镜像仓库">
        <template slot-scope="{row}">
          <span>{{ row.image }}</span>
        </template>
      </el-table-column>

      <el-table-column label="D" width="40" align="center">
        <template slot-scope="{row}">
          <div v-if="row.res.includes('deployment')">
            <i class="el-icon-circle-check" />
          </div>
          <div v-else>
            <i class="el-icon-error" />
          </div>
        </template>
      </el-table-column>
      <el-table-column label="S" width="40" align="center">
        <template slot-scope="{row}">
          <div v-if="row.res.includes('service')">
            <i class="el-icon-circle-check" />
          </div>
          <div v-else>
            <i class="el-icon-error" />
          </div>
        </template>
      </el-table-column>
      <el-table-column label="C" width="40" align="center">
        <template slot-scope="{row}">
          <div v-if="row.res.includes('configmap')">
            <i class="el-icon-circle-check" />
          </div>
          <div v-else>
            <i class="el-icon-error" />
          </div>
        </template>
      </el-table-column>
      <el-table-column label="P" width="40" align="center">
        <template slot-scope="{row}">
          <div v-if="row.res.includes('pdb')">
            <i class="el-icon-circle-check" />
          </div>
          <div v-else>
            <i class="el-icon-error" />
          </div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="创建时间" width="110px">
        <template slot-scope="{row}">
          <span>{{ row.update.split(".")[0].split(/\d\d\d\d-/)[1].split(/:\d\d$/)[0] }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="状态" width="70px">
        <template slot-scope="{row}">
          <el-tag :type="row.deploystatus | statusFilter">
            {{ trstatus[row.deploystatus] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="80px">
        <template slot-scope="{row}">
          <el-button size="mini" type="danger" @click="deldeployms(row.ver, row.env, row.namespace, row.microservice, row.tag)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

import { getAllInfo,  ddService, updateService, delService } from '@/api/consul'

export default {
  name: 'DragTable',
  filters: {
    statusFilter(status) {
      const statusMap = {
        true: 'success',
        false: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      nslist: null,
      nsmslist: null,
      nsmstaglist: null,
      msdict: null,
      total: null,
      listLoading: true,
      fresh: false,
      trstatus: { true: '成功', false: '等待' },
      listQuery: { dpm: '', tag: '', batch: '', resGroup: ['deployment'] },
      reslist: resOptions,
      verlist: ['博世蓬莱-A63', '博世昆仑-A62'],
      batchlist: [1, 2, 3, 4, 5, 6, 7, 8, 9, 99],
      envdict: { 'prod': 'prod生产环境' },
      sortable: null,
      oldList: [],
      newList: []
    }
  },
  computed: {
    cns() {
      return this.listQuery.namespace
    },
    cms() {
      return this.listQuery.dpm
    },
    cver() {
      return this.listQuery.ver
    },
    cenv() {
      return this.listQuery.env
    }
  },
  watch: {
    cns(newns) {
      this.nsmslist = []
      this.listQuery.dpm = ''
      if (newns === '') {
        this.nsmslist = ''
      } else {
        this.nsmslist = this.msdict[newns]
      }
      this.getdeploylist(this.listQuery.ver, this.listQuery.env, newns)
    },
    cms(newms) {
      this.nsmstaglist = []
      this.listQuery.tag = ''
      if (newms === '') {
        this.nsmstaglist = ''
      } else {
        this.nsmstaglist = this.getTag(this.listQuery.namespace, newms)
      }
    },
    cver(newver) {
      this.getdeploylist(newver, this.listQuery.env, this.listQuery.namespace)
    },
    cenv(newenv) {
      this.getdeploylist(this.listQuery.ver, newenv, this.listQuery.namespace)
    }
  },
  created() {
    this.getAllInfo()
  },
  methods: {
    async freshlist() {
      this.fresh = true
      this.getdeploylist(this.listQuery.ver, this.listQuery.env, this.listQuery.namespace)
      setTimeout(() => {
        this.fresh = false
      }, 10000)
    },
    async getdeploylist(qver, qenv, qns) {
      this.listLoading = true
      const { data } = await getDeployList(qver, qenv, qns)
      this.list = data
      this.listLoading = false
    },
    async getList() {
      const { ms, ns } = await mslist()
      this.nslist = ns
      this.msdict = ms
      if (this.$route.params.jver) {
        this.nsmslist = this.msdict[this.listQuery.namespace]
      }
    },
    async getTag(qns, qms) {
      this.listLoading = true
      const { data } = await getimagetag(qns, qms)
      this.nsmstaglist = data
      this.listLoading = false
    },
    async addms(postdata) {
      addMS(postdata).then(response => {
        this.getdeploylist(this.listQuery.ver, this.listQuery.env, this.listQuery.namespace)
        this.$message({
          message: response.data,
          type: response.status
        })
      })
    },
    async deldeployms(dver, denv, dns, dms, dtag) {
      this.$confirm('此操作将删除【' + dver + '_' + denv + '_' + dns + ':' + dms + '】，是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delDeployMS(dver, denv, dns, dms, dtag).then(response => {
          this.$message({
            message: response.data,
            type: 'success'
          })
          this.getdeploylist(this.listQuery.ver, this.listQuery.env, this.listQuery.namespace)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>
