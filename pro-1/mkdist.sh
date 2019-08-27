if test "$2" = "nobuild"
then
	echo $2
else
	npm run build
	echo 'build'
fi
rm -rf ../frontend-test/dist/*
cp -r dist/* ../frontend-test/dist/
cd ../
git add .
git commit -m $1
git push
echo 'done'
