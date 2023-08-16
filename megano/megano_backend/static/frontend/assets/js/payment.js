var mix = {
	methods: {
		submitPayment() {
			const orderId = location.pathname.startsWith('/payment/')
				? Number(location.pathname.replace('/payment/', '').replace('/', ''))
				: null
			console.log({
				name: this.name,
				number: this.number1,
				year: this.year,
				month: this.month,
				code: this.code,
			})
			this.postData(`/api/payment/${orderId}`, {
				name: this.name,
				number: this.number1,
				year: this.year,
				month: this.month,
				code: this.code
			}).then(() => {
				this.number1 = ''
				this.name = ''
				this.year = ''
				this.month = ''
				this.code = ''
				location.assign('/progress-payment')
			}).catch(() => {
				alert('Неверные данные карты')
			})
		}
	},
	data() {
		return {
			number1: '',
			month: '',
			year: '',
			name: '',
			code: ''
		}
	}
}