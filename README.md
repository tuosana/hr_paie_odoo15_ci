# hr_paie_odoo15_ci
#Push de projet(public) sur le github 

echo "# hr_paie_odoo15_ci" >> README.md
git init
git add README.md
git add .
git config --global user.email "tuosana2001@gmail.com"
git config --global user.name "tuosana"
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/tuosana/hr_paie_odoo15_ci.git
git push -u origin main
