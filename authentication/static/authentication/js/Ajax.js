class Ajax {
	constructor(csrfToken) {
		if (typeof csrfToken !== 'undefined' && csrfToken && csrfToken !== '') {
			this.csrfToken = csrfToken;
		} else {
			this.csrfToken = this._getCookie('csrftoken');
		}
	}

	get(uri, data) {
		return new Promise((resolve, reject) => {
			$.ajax({
				url: uri,
				type: 'GET',
				beforeSend: function () {
					$('#loader').show();
				},
				dataType: 'json',
				data: data,
				contentType: 'application/json'
			}).done((responseData) => {
				$('#loader').hide();
				resolve(responseData);
			}).fail((error) => {
				$('#loader').hide();
				reject({
					status: error.status,
					statusText: error.statusText
				});
			});
		});
	}

	post(uri, data) {
		return new Promise((resolve, reject) => {
			$.ajax({
				url: uri,
				type: 'POST',
				dataType: 'json',
				data: data,
				contentType: 'application/json',
				beforeSend: (xhr) => {
					$('#loader').show();
					xhr.setRequestHeader('X-CSRFToken', this.csrfToken);
					xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
				}
			}).done((responseData) => {
				$('#loader').hide();
				resolve(responseData);
			}).fail((error) => {
				$('#loader').hide();
				reject({
					status: error.status,
					statusText: error.statusText
				});
			});
		});
	}

	put(uri, data) {
		return new Promise((resolve, reject) => {
			$.ajax({
				url: uri,
				type: 'PUT',
				dataType: 'json',
				data: data,
				contentType: 'application/json',
				beforeSend: (xhr) => {
					$('#loader').show();
					xhr.setRequestHeader('X-CSRFToken', this.csrfToken);
					xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
				}
			}).done((responseData) => {
				$('#loader').hide();
				resolve(responseData);
			}).fail((error) => {
				$('#loader').hide();
				reject({
					status: error.status,
					statusText: error.statusText
				});
			});
		});
	}

	delete(uri, data) {
		return new Promise((resolve, reject) => {
			$.ajax({
				url: uri,
				type: 'DELETE',
				dataType: 'json',
				data: data,
				contentType: 'application/json',
				beforeSend: (xhr) => {
					$('#loader').show();
					xhr.setRequestHeader('X-CSRFToken', this.csrfToken);
					xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
				}
			}).done((responseData) => {
				$('#loader').hide();
				resolve(responseData);
			}).fail((error) => {
				$('#loader').hide();
				reject({
					status: error.status,
					statusText: error.statusText
				});
			});
		});
	}

	_getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
}

export default Ajax