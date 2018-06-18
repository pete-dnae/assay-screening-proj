import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Login',
  data() {
    return {
      username: null,
      password: null,
    };
  },
  computed: {
    ...mapGetters({
      error: 'getLoginError',
    }),
  },
  methods: {
    ...mapActions(['obtainToken']),
    handleSubmit() {
      this.obtainToken({
        username: this.username,
        password: this.password,
      }).then(() => {
        this.$router.push('/experiment');
      });
    },
  },
};
