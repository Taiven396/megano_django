var mix = {
	methods: {
		signUp () {
			const name = document.querySelector('#name').value
			const username = document.querySelector('#login').value
			const password = document.querySelector('#password').value
			const email = document.querySelector('#email').value
			this.postData('/api/sign-up', JSON.stringify({ name, username, password, email }))
				.then(({ data, status }) => {
					location.assign(`/code`)
				})
				.catch(() => {
					alert('Ошибка авторизации!')
				})
		}
	},
	mounted() {
	},
	data() {
		return {}
	}
}