from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='project',
            name='store_link',
            field=models.URLField(blank=True, null=True, help_text='App Store / Play Store / Live URL'),
        ),
    ]
