def register():
    excel_file = 'users.xlsx'

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            flash('Please fill out all fields.')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        # Check if Excel file exists, create if not
        if not os.path.exists(excel_file):
            wb = Workbook()
            ws = wb.active
            ws.title = "Users"
            ws.append(['Username', 'Email', 'Password'])
            wb.save(excel_file)

        # Load workbook and check for existing username
        wb = openpyxl.load_workbook(excel_file)
        ws = wb['Users']

        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] == username:
                flash('Username already exists.')
                wb.close()
                return redirect(url_for('register'))

        # Append new user data
        ws.append([username, email, password])
        wb.save(excel_file)
        wb.close()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
