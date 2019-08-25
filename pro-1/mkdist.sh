if [$2 -eq 'nobuild']
then
	echo $2
else
	# npm run build
	# rm -rf ../frontend-test/dist/*
	# cp -r dist/* ../frontend-test/dist/
	echo 'build'
echo $2
fi
cd ../
git add .
git commit -m $1
git push
echo 'done'
