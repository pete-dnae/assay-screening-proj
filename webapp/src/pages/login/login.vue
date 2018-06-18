<template>
<div class="container mt-5">
      <h2>Log In</h2>
      <i class="fa fa-user-circle-o fa-5x d-block" aria-hidden="true"></i>
      <small >Log in to your account to view current tab.</small>      
      <div class="alert alert-danger" v-if="error">
        <p>{{ error }}</p>
      </div>
      
        <div class="row">
          <div class="col-md-3">
          </div>
          <div class="form-group col-6">
              <input
                type="text"
                class="form-control"
                placeholder="Enter your username"
                v-model="username"          
              >
           </div>
           </div>
          <div class="row">
            <div class="col-md-3">
            </div>
            <div class="form-group col-6">
                <input
                  type="password"
                  class="form-control"
                  placeholder="Enter your password"
                  v-model="password"
                >
            </div>
          </div>
      <button class="btn btn-primary"
       @click="handleSubmit()"
       :disabled="!(username&&password)">
        Access</button>
    </div>
</template>
<script src='./login.js'></script>