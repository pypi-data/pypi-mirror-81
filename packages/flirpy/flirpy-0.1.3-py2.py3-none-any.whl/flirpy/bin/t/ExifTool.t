# Before "make install", this script should be runnable with "make test".
# After "make install" it should work as "perl t/ExifTool.t".

BEGIN {
    $| = 1; print "1..31\n"; $Image::ExifTool::configFile = '';
    require './t/TestLib.pm'; t::TestLib->import();
}
END {print "not ok 1\n" unless $loaded;}

# test 1: Load the module(s)
use Image::ExifTool 'ImageInfo';
$loaded = 1;
print "ok 1\n";

my $testname = 'ExifTool';
my $testnum = 1;

# test 2: extract information from JPG file using name
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    my $info = $exifTool->ImageInfo('t/images/ExifTool.jpg');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 3: TIFF file using file reference and ExifTool object with options
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(Duplicates => 1, Unknown => 1);
    open(TESTFILE, 't/images/ExifTool.tif');
    my $info = $exifTool->ImageInfo(\*TESTFILE);
    close(TESTFILE);
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 4: test the Group option to extract EXIF info only
{
    ++$testnum;
    my $info = ImageInfo('t/images/Canon.jpg', {Group0 => 'EXIF'});
    print 'not ' unless check($info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 5: extract specified tags only
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
# don't test DateFormat because strftime output varies with locale
#    $exifTool->Options(DateFormat => '%H:%M:%S %a. %b. %e, %Y');
    my @tags = ('CreateDate', 'DateTimeOriginal', 'ModifyDate', 'Orientation#', '?Resolution');
    my $info = $exifTool->ImageInfo('t/images/Canon.jpg', \@tags);
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 6: test the 5 different ways to exclude tags...
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(Exclude => 'ImageWidth');
    my @tagList = ( '-ImageHeight', '-Make' );
    my $info = $exifTool->ImageInfo('t/images/Canon.jpg', '-FileSize', '-*resolution',
                        \@tagList, {Group0 => '-MakerNotes'});
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# tests 7/8: test ExtractInfo(), GetInfo(), CombineInfo()
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(Duplicates => 0);  # don't allow duplicates
    $exifTool->ExtractInfo('t/images/Canon.jpg');
    my $info1 = $exifTool->GetInfo({Group0 => 'MakerNotes'});
    my $info2 = $exifTool->GetInfo({Group0 => 'EXIF'});
    my $info = $exifTool->CombineInfo($info1, $info2);
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";

    # combine information in different order
    ++$testnum;
    $info = $exifTool->CombineInfo($info2, $info1);
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 9: test group options across different families
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    my $info = $exifTool->ImageInfo('t/images/Canon.jpg',
                    { Group1 => 'Canon', Group2 => '-Camera' });
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# tests 10/11: test ExtractInfo() and GetInfo()
# (uses output from test 5 for comparison)
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
# don't test DateFormat because strftime output is system dependent
#    $exifTool->Options(DateFormat => '%H:%M:%S %a. %b. %e, %Y');
    $exifTool->ExtractInfo('t/images/Canon.jpg');
    my @tags = ('createdate', 'datetimeoriginal', 'modifydate', 'orientation#', '?resolution');
    my $info = $exifTool->GetInfo(\@tags);
    my $good = 1;
    my @expectedTags = ('CreateDate', 'DateTimeOriginal', 'ModifyDate', 'Orientation',
                        'XResolution', 'YResolution');
    for (my $i=0; $i<scalar(@tags); ++$i) {
        $tags[$i] = $expectedTags[$i] or $good = 0;
    }
    print 'not ' unless $good;
    print "ok $testnum\n";

    ++$testnum;
    print 'not ' unless check($exifTool, $info, $testname, $testnum, 5);
    print "ok $testnum\n";
}

# tests 12/13: check precidence of tags extracted from groups
# (Note: these tests should produce the same output as 7/8,
#  so the .out files from tests 7/8 are used)
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(Duplicates => 0);  # don't allow duplicates
    my $info = $exifTool->ImageInfo('t/images/Canon.jpg',{Group0=>['MakerNotes','EXIF']});
    print 'not ' unless check($exifTool, $info, $testname, $testnum, 7);
    print "ok $testnum\n";

    # combine information in different order
    ++$testnum;
    $info = $exifTool->ImageInfo('t/images/Canon.jpg',{Group0=>['EXIF','MakerNotes']});
    print 'not ' unless check($exifTool, $info, $testname, $testnum, 8);
    print "ok $testnum\n";
}

# tests 14/15/16: test GetGroups()
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->ExtractInfo('t/images/Canon.jpg');
    my @groups = $exifTool->GetGroups(2);
    my $not;
    foreach ('Camera','ExifTool','Image','Time') {
        $_ eq shift @groups or $not = 1;
    }
    @groups and $not = 1;
    print 'not ' if $not;
    print "ok $testnum\n";
    
    ++$testnum;
    my $info = $exifTool->GetInfo({Group0 => 'EXIF'});
    @groups = $exifTool->GetGroups($info,0);
    print 'not ' unless @groups==1 and $groups[0] eq 'EXIF';
    print "ok $testnum\n";

    ++$testnum;
    my $testfile = "t/ExifTool_$testnum";
    open(TESTFILE,">$testfile.failed");
    my $oldSep = $/;   
    $/ = "\x0a";        # set input line separator
    $exifTool->ExtractInfo('t/images/Canon.jpg');
    my $family = '1:2';
    @groups = $exifTool->GetGroups($family);
    my $group;
    foreach $group (@groups) {
        next if $group eq 'ExifTool';
        print TESTFILE "---- $group ----\n";
        my $info = $exifTool->GetInfo({"Group$family" => $group});
        foreach (sort $exifTool->GetTagList($info)) {
            print TESTFILE "$_ : $$info{$_}\n";
        } 
    }
    $/ = $oldSep;       # restore input line separator
    close(TESTFILE);
    print 'not ' unless testCompare("$testfile.out","$testfile.failed",$testnum);
    print "ok $testnum\n";
}

# test 17: Test verbose output
{
    ++$testnum;
    print 'not ' unless testVerbose($testname, $testnum, 't/images/Canon.jpg', 3);
    print "ok $testnum\n";
}

# tests 18/19: Test Group# option with multiple groups and no duplicates
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(Duplicates => 0);  # don't allow duplicates
    my $info = $exifTool->ImageInfo('t/images/Canon.jpg',
                    { Group0 => ['MakerNotes','EXIF'] });
    print 'not ' unless check($exifTool, $info, $testname, $testnum, 7);
    print "ok $testnum\n";

    ++$testnum;
    $info = $exifTool->ImageInfo('t/images/Canon.jpg',
                    { Group0 => ['EXIF','MakerNotes'] });
    print 'not ' unless check($exifTool, $info, $testname, $testnum, 8);
    print "ok $testnum\n";
}

# test 20: Test extracting a single, non-priority tag with duplicates set to 0
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(Duplicates => 0);
    my $info = $exifTool->ImageInfo('t/images/Canon.jpg', 'EXIF:WhiteBalance');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 21: Test extracting ICC_Profile as a block
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    my $info = $exifTool->ImageInfo('t/images/ExifTool.tif', 'ICC_Profile');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 22: Test InsertTagValues
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    my @foundTags;
    $exifTool->ImageInfo('t/images/ExifTool.jpg', \@foundTags);
    my $str = $exifTool->InsertTagValues(\@foundTags, '${ifd0:model;tr/i/_/} - $1ciff:3main:model');
    my $testfile = "t/ExifTool_$testnum";
    open(TESTFILE,">$testfile.failed");
    my $oldSep = $/;   
    $/ = "\x0a";        # set input line separator
    print TESTFILE $str, "\n";
    $/ = $oldSep;       # restore input line separator
    close(TESTFILE);
    print 'not ' unless testCompare("$testfile.out","$testfile.failed",$testnum);
    print "ok $testnum\n";
}

# test 23: Test the multi-group feature in a tag name
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    my $info = $exifTool->ImageInfo('t/images/ExifTool.jpg', 'main:Author:IPTC3:all');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 24: Test a shortcut with multiple group names and a ValueConv suffix
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    my $info = $exifTool->ImageInfo('t/images/Canon.jpg', 'exififd:camera:common#');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 25: Test GlobalTimeShift option
{
    ++$testnum;
    if (eval { require Time::Local }) {
        my $exifTool = new Image::ExifTool;
        $exifTool->Options(GlobalTimeShift => '-0:1:0 0:0:0');
        # Note: can't extract system times because this could result in a different
        # calculated global time offset (since I am shifting by 1 month)
        my $info = $exifTool->ImageInfo('t/images/ExifTool.jpg', 'time:all', '-system:all');
        print 'not ' unless check($exifTool, $info, $testname, $testnum);
        print "ok $testnum\n";
    } else {
        print "ok $testnum # skip Requires Time::Local\n";
    }
}

# test 26: Test wildcards using '#' suffix with duplicate PrintConv tags and exclusions
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    # (hack to avoid sorting in TestLib.pm because order of duplicate tags would be indeterminate)
    $$exifTool{NO_SORT} = 1;
    my $info = $exifTool->ImageInfo('t/images/Canon.jpg', 'encodingprocess', 'E*#', 'exposureMode',
                                    '-ExifVersion');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 27: Test ListItem option
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(ListItem => -3);
    my $info = $exifTool->ImageInfo('t/images/ExifTool.jpg', 'Subject', 'SupplementalCategories');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 28: Test FastScan = 3
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(FastScan => 3);
    my $info = $exifTool->ImageInfo('t/images/ExifTool.jpg');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 29: Test Filter
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    $exifTool->Options(Filter => 'tr/ /_/;tr/0-9/#/');
    my $info = $exifTool->ImageInfo('t/images/ExifTool.jpg', '-ExifToolVersion');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# test 30: Calculate JPEGDigest and JPEGQualityEstimate
{
    ++$testnum;
    my $skip = '';
    if (eval 'require Digest::MD5') {
        my $exifTool = new Image::ExifTool;
        my $info = $exifTool->ImageInfo('t/images/Writer.jpg', 'JPEGDigest', 'JPEGQualityEstimate');
        print 'not ' unless check($exifTool, $info, $testname, $testnum);
    } else {
        $skip = ' # skip Requires Digest::MD5';
    }
    print "ok $testnum$skip\n";
}

# test 31: Test Validate feature
{
    ++$testnum;
    my $exifTool = new Image::ExifTool;
    my $info = $exifTool->ImageInfo('t/images/CanonRaw.cr2', 'Validate', 'Warning', 'Error');
    print 'not ' unless check($exifTool, $info, $testname, $testnum);
    print "ok $testnum\n";
}

# end
