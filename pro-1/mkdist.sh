npm run build
rm -rf ../frontend-test/dist/*
cp -r dist/* ../frontend-test/dist/
cd ../
git add .
git commit -m $1
git push