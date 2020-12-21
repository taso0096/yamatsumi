<template>
  <v-card
    v-if="$route.query.redirect && !$_userData.isLoaded"
    flat
    color="rgba(0, 0, 0, 0)"
  >
    <v-card-text class="text-center">
      <div class="body-1 mb-3">
        Loging in
      </div>
      <v-progress-circular
        indeterminate
        color="primary"
      />
    </v-card-text>
  </v-card>
  <v-card
    v-else
    outlined
    max-width="500"
  >
    <v-card-title>
      <span class="mx-auto display-1">YAMATSUMI</span>
    </v-card-title>
    <v-card-text>
      <v-form v-model="isFormValid">
        <v-text-field
          v-model="loginForm.username"
          :rules="[rules.required]"
          label="Username"
          required
        ></v-text-field>

        <v-text-field
          v-model="loginForm.password"
          :rules="[rules.required]"
          label="Password"
          type="password"
          required
        ></v-text-field>

        <v-row>
          <v-col>
            <v-btn
              @click.prevent="doLogin"
              block
              depressed
              :disabled="!isFormValid"
              :loading="isLoadingLogin"
              color="primary"
              type="submit"
            >Login</v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<style lang="scss" scoped>
.v-card {
  margin: auto;
}
</style>

<script>
import axios from '@/axios/index';

export default {
  name: 'Login',
  data: () => ({
    isFormValid: false,
    isLoadingLogin: false,
    loginForm: {
      username: '',
      password: ''
    },
    rules: {
      required: v => !!v?.length
    }
  }),
  methods: {
    async doLogin() {
      this.isLoadingLogin = true;
      const loginForm = this.loginForm;
      const accessToken = await axios
        .post('/users/login', loginForm, {
          validateStatus: status => {
            return status < 500;
          }
        })
        .then(res => {
          if (res.status !== 200) {
            this.$_pushNotice('ユーザ名またはパスワードが違います。', 'error');
            return false;
          }
          return res.data.token;
        })
        .catch(async() => {
          this.$_pushNotice('エラーが発生しました。', 'error');
          return false;
        });
      if (accessToken) {
        await axios
          .get('/users/verify', {
            headers: {
              Authorization: `JWT ${accessToken}`
            }
          })
          .then(res => {
            this.$store.dispatch('updateAuthState', {
              accessToken,
              ...res.data
            });
            this.$_pushNotice('ログインに成功しました。', 'success');
            this.$router.push(this.$route.query.redirect || { name: 'Network' });
            console.log(res.data);
          })
          .catch(() => {
            this.$store.dispatch('updateAuthState', {});
            this.$_pushNotice('エラーが発生しました。', 'error');
          });
      }
      this.isLoadingLogin = false;
    }
  }
};
</script>
